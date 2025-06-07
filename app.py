import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
import base64

client = OpenAI()

# 函數：編碼圖片為 base64
def encode_image(image_path):
    """將圖片文件編碼為 base64 字符串"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# 函數：清理檔案路徑
def clean_file_path(file_path):
    """清理文件路徑，移除 Unicode 字符並標準化路徑"""
    # 移除 Unicode 窄不間斷空格和其他可能的問題字符
    cleaned_path = file_path.replace('\u202f', ' ')  # 窄不間斷空格
    cleaned_path = cleaned_path.replace('\u00a0', ' ')  # 不間斷空格
    
    # 標準化路徑
    cleaned_path = os.path.normpath(cleaned_path)
    
    return cleaned_path

# === 圖片上傳後送 GPT 分析並命名 ===
def generate_filename(image_path):
    try:
        base64_image = encode_image(image_path)
        response = client.responses.create(
            model="gpt-4.1",
            input = [
                {
                    "role": "user",
                    "content": [
                        { "type": "input_text", "text": "You are a great file name generator. Please analyze the image and return the name of the image in English, and use a hyphen to separate words, for example: meeting-summary-zoom. Don't include any other text in your response, just the name of the image." },
                        {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
                }
            ]
        )
        return response.output_text
    except Exception as e:
        print(f"❌ GPT API Error: {e}")
        return None

# === 檔案事件處理器 ===
class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.processed_files = set()  # 追蹤已處理的文件，避免重複處理
    
    def process_screenshot(self, file_path, event_type="created"):
        """處理截圖文件的核心邏輯"""
        print(f"🐛 DEBUG - Original path: {repr(file_path)}")
        
        # 生成多個可能的路徑版本來嘗試
        path_variants = [
            file_path,  # 原始路徑
            clean_file_path(file_path),  # 清理後的路徑
            os.path.normpath(file_path),  # 標準化路徑
        ]
        
        # 找到真正存在的文件路徑
        actual_path = None
        for variant in path_variants:
            print(f"🐛 DEBUG - Trying path: {repr(variant)}")
            if os.path.exists(variant):
                actual_path = variant
                print(f"✅ Found existing file: {repr(actual_path)}")
                break
        
        # 如果還是找不到，嘗試在目錄中搜索相似文件
        if actual_path is None:
            directory = os.path.dirname(file_path)
            filename_base = os.path.basename(file_path)
            
            # 移除文件名中的特殊字符來匹配
            clean_filename = filename_base.replace('\u202f', '').replace('\u00a0', '').replace('  ', ' ')
            
            try:
                files_in_dir = os.listdir(directory)
                print(f"🐛 DEBUG - Looking for similar files in directory...")
                
                for file in files_in_dir:
                    if file.lower().endswith('.png') and 'screenshot' in file.lower():
                        # 比較文件名（忽略特殊字符）
                        clean_existing = file.replace('\u202f', '').replace('\u00a0', '').replace('  ', ' ')
                        
                        if (clean_existing.lower() == clean_filename.lower() or
                            # 也嘗試基於時間戳匹配
                            ('4.25.00' in file and 'PM' in file and '2025-06-07' in file)):
                            
                            actual_path = os.path.join(directory, file)
                            print(f"🔄 Found matching file: {repr(file)}")
                            print(f"✅ Using path: {repr(actual_path)}")
                            break
                            
            except Exception as search_error:
                print(f"🐛 DEBUG - Directory search error: {search_error}")
        
        # 如果還是找不到文件，放棄
        if actual_path is None:
            print(f"❌ Could not find file after trying all variants")
            return
        
        original_path = actual_path
        
        # 檢查文件是否為 PNG 格式
        if not original_path.lower().endswith(".png"):
            return
        
        # 獲取檔案名稱
        filename = os.path.basename(original_path)
        
        # 檢查是否已經處理過這個文件
        if original_path in self.processed_files:
            print(f"🔍 Already processed: {filename}")
            return
        
        # 如果是隱藏文件，先記錄但不處理
        if filename.startswith('.'):
            print(f"🔍 Detected temporary file ({event_type}): {filename}")
            return
        
        # 檢查檔名是否包含 "Screenshot"（確保是截圖文件）
        if "screenshot" not in filename.lower():
            print(f"🚫 Not a screenshot file: {filename}")
            return
        
        print(f"📸 Processing screenshot ({event_type}): {original_path}")
        
        # 將文件加入已處理清單
        self.processed_files.add(original_path)
        
        # 驗證文件狀態
        try:
            size = os.path.getsize(original_path)
            print(f"✅ File confirmed: {size} bytes")
            
            if size == 0:
                print(f"⚠️ File is empty, waiting for content...")
                time.sleep(1)
                size = os.path.getsize(original_path)
                print(f"✅ File size after wait: {size} bytes")
                
        except Exception as stat_error:
            print(f"❌ Error getting file info: {stat_error}")
            self.processed_files.discard(original_path)
            return
        
        # 添加一個小延遲確保文件穩定
        time.sleep(0.5)
        
        try:
            # 生成新檔名
            new_name = generate_filename(original_path)
            
            if new_name is None:
                print("❌ Failed to generate new filename, keeping original name")
                return
            
            # 清理生成的檔名（移除可能的特殊字符）
            new_name = new_name.strip().replace(' ', '-')
            
            # 創建新路徑
            directory = os.path.dirname(original_path)
            new_path = os.path.join(directory, f"{new_name}.png")
            
            print(f"🔍 New name: {new_name}")
            
            # 確保新檔名不會與現有檔案衝突
            counter = 1
            while os.path.exists(new_path):
                new_path = os.path.join(directory, f"{new_name}-{counter}.png")
                counter += 1
            
            # 重新命名檔案
            os.rename(original_path, new_path)
            print(f"✅ Successfully renamed to: {new_path}")
            
        except Exception as e:
            print(f"❌ Error processing file: {e}")
            print(f"   Original path: {original_path}")
            self.processed_files.discard(original_path)  # 從處理清單中移除
    
    def on_created(self, event):
        """當文件被創建時觸發"""
        if event.is_directory:
            return
        self.process_screenshot(event.src_path, "created")
    
    def on_moved(self, event):
        """當文件被移動/重命名時觸發"""
        if event.is_directory:
            return
        
        # 檢查是否是從隱藏文件變為正式文件
        src_filename = os.path.basename(event.src_path)
        dest_filename = os.path.basename(event.dest_path)
        
        # 如果是從隱藏文件重命名為正式文件
        if src_filename.startswith('.') and not dest_filename.startswith('.'):
            print(f"🔄 File renamed from temporary to final: {dest_filename}")
            self.process_screenshot(event.dest_path, "moved")
        else:
            # 其他移動事件也處理
            self.process_screenshot(event.dest_path, "moved")
    
    def on_modified(self, event):
        """當文件被修改時觸發（有時截圖創建會觸發此事件）"""
        if event.is_directory:
            return
        
        # 只處理剛創建的文件的修改事件
        file_path = clean_file_path(event.src_path)
        filename = os.path.basename(file_path)
        
        # 如果是截圖文件且還沒處理過
        if ("screenshot" in filename.lower() and 
            file_path not in self.processed_files and 
            not filename.startswith('.')):
            print(f"📝 Screenshot modified: {filename}")
            self.process_screenshot(event.src_path, "modified")

# === 啟動監控 ===
if __name__ == "__main__":
    watch_dir = os.path.expanduser("~/Desktop/Screenshots")
    
    # 確保監控目錄存在
    if not os.path.exists(watch_dir):
        print(f"❌ Watch directory does not exist: {watch_dir}")
        print("Please create the Screenshots directory first.")
        exit(1)
    
    observer = Observer()
    observer.schedule(ScreenshotHandler(), path=watch_dir, recursive=False)
    observer.start()
    print(f"👀 Watching for screenshots in: {watch_dir}")
    print("Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping screenshot monitor...")
        observer.stop()
    observer.join()
    print("👋 Screenshot monitor stopped.")