#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script để kiểm tra integration giữa gui.py và ganjingworld_uploader.py
"""

import sys
import os

# Add module path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test import các module"""
    print("\n=== TEST 1: IMPORTS ===")
    try:
        from ganjingworld_uploader import GanjingworldUploader
        print("OK: GanjingworldUploader imported")
        
        from gui import DownloaderGUI, LogSignal
        print("OK: gui imported")
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_uploader_class():
    """Test GanjingworldUploader class"""
    print("\n=== TEST 2: GanjingworldUploader CLASS ===")
    try:
        from ganjingworld_uploader import GanjingworldUploader
        
        # Test initialization
        access_token = "test_token"
        channel_id = "test_channel"
        uploader = GanjingworldUploader(access_token, channel_id)
        
        print(f"OK: Uploader initialized with token and channel")
        
        # Test methods exist
        methods = [
            'get_upload_token',
            'extract_thumbnail',
            'upload_thumbnail',
            'create_content',
            'upload_video',
            'check_upload_status',
            'wait_for_processing',
            'upload_workflow',
            'set_log_callback',
            'log'
        ]
        
        for method in methods:
            if hasattr(uploader, method):
                print(f"OK: Method '{method}' exists")
            else:
                print(f"ERROR: Method '{method}' missing")
                return False
        
        # Test log callback
        logs = []
        uploader.set_log_callback(lambda msg: logs.append(msg))
        uploader.log("Test message")
        if logs and logs[0] == "Test message":
            print("OK: Log callback works")
        else:
            print("ERROR: Log callback failed")
            return False
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_gui_attributes():
    """Test GUI attributes"""
    print("\n=== TEST 3: GUI ATTRIBUTES ===")
    try:
        import ast
        
        with open('gui.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Check required attributes in __init__
        required_attrs = [
            'self.last_downloaded_file',
            'self.gjw_checkbox',
            'self.gjw_token_input',
            'self.gjw_channel_input'
        ]
        
        for attr in required_attrs:
            if attr in code:
                print(f"OK: Attribute '{attr}' present in code")
            else:
                print(f"ERROR: Attribute '{attr}' missing")
                return False
        
        # Check required methods
        required_methods = [
            'on_gjw_checkbox_changed',
            'upload_to_ganjingworld',
            'perform_upload'
        ]
        
        for method in required_methods:
            if f'def {method}' in code:
                print(f"OK: Method '{method}' defined")
            else:
                print(f"ERROR: Method '{method}' missing")
                return False
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_credentials_handling():
    """Test credentials handling logic"""
    print("\n=== TEST 4: CREDENTIALS HANDLING ===")
    try:
        from ganjingworld_uploader import GanjingworldUploader
        
        # Test with valid credentials
        valid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test"
        valid_channel = "1frk2ne41b04vrB9rtsk4yYgK1mo0c"
        
        uploader = GanjingworldUploader(valid_token, valid_channel)
        
        if uploader.access_token == valid_token:
            print("OK: Access token stored correctly")
        else:
            print("ERROR: Access token not stored")
            return False
        
        if uploader.channel_id == valid_channel:
            print("OK: Channel ID stored correctly")
        else:
            print("ERROR: Channel ID not stored")
            return False
        
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("GANJINGWORLD INTEGRATION TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Uploader Class", test_uploader_class),
        ("GUI Attributes", test_gui_attributes),
        ("Credentials Handling", test_credentials_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\nEXCEPTION in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
