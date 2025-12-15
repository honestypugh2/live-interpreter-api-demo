#!/usr/bin/env python3
"""
Generate all Streamlit architecture diagrams
Creates visual diagrams using the diagrams library with Azure icons
"""
import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a diagram generation script"""
    print(f"\n{'='*70}")
    print(f"🎨 {description}")
    print('='*70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(e.stderr)
        return False

def main():
    """Generate all diagrams"""
    print("\n" + "="*70)
    print("🏗️  Streamlit Architecture Diagram Generator")
    print("    Azure Live Interpreter API Demo")
    print("="*70)
    
    scripts = [
        ("generate_streamlit_architecture.py", "Generating Streamlit Monolithic Architecture Diagram"),
        ("generate_dataflow.py", "Generating Streamlit Continuous Translation Flow Diagram"),
        ("generate_react_architecture.py", "Generating React Client-Server Architecture Diagram"),
        ("generate_react_websocket_flow.py", "Generating React WebSocket Message Flow Diagram"),
    ]
    
    results = {}
    for script, desc in scripts:
        script_path = Path(script)
        if script_path.exists():
            results[script] = run_script(script, desc)
        else:
            print(f"\n⚠️  Script not found: {script}")
            results[script] = False
    
    # Summary
    print("\n" + "="*70)
    print("📊 Generation Summary")
    print("="*70)
    
    for script, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {script}")
    
    success_count = sum(results.values())
    total_count = len(scripts)
    
    print("="*70)
    
    if success_count == total_count:
        print(f"\n🎉 Success! Generated {success_count}/{total_count} diagrams")
        print("\n📁 Generated Files:")
        print("   📄 Streamlit Architecture Diagrams:")
        print("      • ../images/streamlit_monolithic_architecture.png")
        print("        → Monolithic architecture with all layers and components")
        print("      • ../images/streamlit_continuous_flow.png")
        print("        → Continuous translation workflow and data flow")
        print("\n   📄 React Architecture Diagrams:")
        print("      • ../images/react_client_server_architecture.png")
        print("        → Client-server architecture with WebSocket communication")
        print("      • ../images/react_websocket_flow.png")
        print("        → WebSocket message flow sequence")
        print("\n📖 Documentation:")
        print("   📘 docs/StreamlitArchitectureDiagrams.md")
        print("      → Streamlit architecture guide with technical details")
        print("   📘 docs/ReactArchitectureDiagrams.md")
        print("      → React architecture guide with WebSocket patterns")
        print("\n💡 View the diagrams:")
        print("   • Open PNG files directly in VS Code or image viewer")
        print("   • Read the markdown documentation for detailed explanations")
        print("   • Share diagrams in presentations and documentation")
        return 0
    else:
        print(f"\n⚠️  Generated {success_count}/{total_count} diagrams")
        print("   Some diagrams failed. Check errors above.")
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure GraphViz is installed: https://graphviz.org/download/")
        print("   2. Verify 'diagrams' package: pip install diagrams")
        print("   3. Check Python version (3.10+ recommended)")
        return 1

if __name__ == "__main__":
    sys.exit(main())
