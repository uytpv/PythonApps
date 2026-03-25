#!/usr/bin/env python3
"""Download Wan2.2-I2V-A14B model from Hugging Face"""

from huggingface_hub import snapshot_download
import os
import sys

def download_model():
    model_repo = "Wan-AI/Wan2.2-I2V-A14B"
    local_dir = "Wan2.2-I2V-A14B"
    
    print(f"📥 Downloading {model_repo}...")
    print(f"📁 Destination: {os.path.abspath(local_dir)}")
    print()
    
    try:
        downloaded_path = snapshot_download(
            repo_id=model_repo,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            repo_type="model"
        )
        
        print(f"\n✅ Download completed successfully!")
        print(f"📍 Model location: {downloaded_path}")
        
        # List directory contents
        if os.path.exists(local_dir):
            files = os.listdir(local_dir)
            print(f"\n📦 Contents ({len(files)} items):")
            for item in sorted(files)[:15]:
                item_path = os.path.join(local_dir, item)
                if os.path.isdir(item_path):
                    print(f"   📁 {item}/")
                else:
                    size_mb = os.path.getsize(item_path) / (1024 * 1024)
                    if size_mb > 1024:
                        print(f"   📄 {item} ({size_mb/1024:.2f} GB)")
                    else:
                        print(f"   📄 {item} ({size_mb:.2f} MB)")
            
            if len(files) > 15:
                print(f"   ... and {len(files) - 15} more items")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error downloading model: {e}")
        print(f"\nTroubleshooting:")
        print(f"1. Check your internet connection")
        print(f"2. Make sure you have enough disk space (model is ~20GB)")
        print(f"3. If this is the first time, it may take several minutes")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
