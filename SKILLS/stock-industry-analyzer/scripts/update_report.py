import json
import os

def update_report(json_path, template_path, output_path):
    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        return
    if not os.path.exists(template_path):
        print(f"Error: Template file not found at {template_path}")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        stock_data = json.load(f)

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    js_data = f"const stockData = {json.dumps(stock_data, ensure_ascii=False, indent=4)};"
    final_html = template.replace("// STOCK_DATA_PLACEHOLDER", js_data)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"✅ Successfully updated report at {output_path}")
    print(f"Total stocks: {len(stock_data)}")

if __name__ == "__main__":
    import sys
    # Default paths for internal use within the skill
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(script_dir)
    
    json_p = os.path.join(skill_root, "references", "stock_analysis.json")
    temp_p = os.path.join(skill_root, "assets", "report_template.html")
    out_p = "D:/gemini/Investment_Report.html"
    
    update_report(json_p, temp_p, out_p)
