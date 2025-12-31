import sys
import os

# Fix path
sys.path.append(os.getcwd())

from src.analysis.builder import ContextBuilder

def test_analysis():
    print("Testing Analysis on Current Directory...")
    root_dir = os.getcwd()
    
    try:
        builder = ContextBuilder(root_dir)
        repo_map = builder.build_repository_map()
        
        print("\n--- REPOSITORY MAP GENERATED ---")
        print(f"Length: {len(repo_map)} chars")
        print("First 500 chars:")
        print(repo_map[:500])
        print("\nTest Passed!")
        
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analysis()
