#!/usr/bin/env python3
"""Rebrand all 50 sites with new single-word names and remove Assets links."""

import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DEMO_ROOT = ROOT / "demo-sites"

# Site name mapping: old name -> new name
BRAND_MAP = {
    "AsterCare": "Aster",
    "HelixNova": "Helix",
    "LumaStudio": "Luma",
    "NexusOps": "Nexus",
    "OrbitDesk": "Orbit",
    "SignalNorth": "Signal",
    "CipherWard": "Cipher",
    "PrismBI": "Prism",
    "HarborLedger": "Harbor",
    "Shieldline": "Shield",
    "CivicLex": "Legal",
    "LedgerFlow": "Ledger",
    "VectorNorth": "Vector",
    "BrightPath": "Bright",
    "TalentBridge": "Talent",
    "UrbanNest": "Urban",
    "ForgeBuild": "Forge",
    "AtelierGrid": "Craft",
    "RoomMuse": "Room",
    "LineWorks": "Line",
    "CoreSystems": "Core",
    "SunVault": "Vault",
    "ClearGrid": "Clear",
    "TerraMetric": "Terra",
    "Fieldwise": "Field",
    "HarvestPack": "Grain",
    "TableFlame": "Table",
    "StayHaven": "Stay",
    "AtlasKind": "Atlas",
    "RideSure": "Ride",
    "ChainPilot": "Chain",
    "MotorArc": "Motor",
    "AeroVector": "Aero",
    "HarborLine": "Port",
    "CornerGoods": "Corner",
    "MarketPulse": "Market",
    "LineaMode": "Linea",
    "SkinTheory": "Skin",
    "WaveCast": "Wave",
    "StageCurrent": "Stage",
    "IndexHouse": "Index",
    "SignalCraft": "Spark",
    "StudioFrame": "Studio",
    "PulseClub": "Pulse",
    "VowVenue": "Vow",
    "CivicAccess": "Forum",
    "CommonGood": "Good",
    "PawHealth": "Paw",
    "MaisonVale": "Maison",
    "Nameplate": "Brand",
}

def replace_brand_in_content(content, old_brand, new_brand):
    """Replace brand name in content, handling various contexts."""
    # Replace in HTML content, titles, descriptions, etc.
    content = content.replace(old_brand, new_brand)
    return content

def remove_assets_link(content):
    """Remove Assets link from HTML content."""
    # Remove Assets link from navigation
    content = re.sub(r'<a[^>]*href=["\']asset-system\.html["\'][^>]*>Assets</a>', '', content)
    content = re.sub(r'<a[^>]*>\s*Assets\s*</a>', '', content)
    return content

def process_html_file(file_path, brand_map):
    """Process an HTML file to update branding and remove Assets links."""
    try:
        content = file_path.read_text(encoding='utf-8')
        original = content
        
        # Replace all brand names
        for old_brand, new_brand in brand_map.items():
            content = replace_brand_in_content(content, old_brand, new_brand)
        
        # Remove Assets links
        content = remove_assets_link(content)
        
        # Write back if changed
        if content != original:
            file_path.write_text(content, encoding='utf-8')
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def process_json_file(file_path, brand_map):
    """Process a JSON file (like site.config.json) to update siteName."""
    try:
        content = file_path.read_text(encoding='utf-8')
        data = json.loads(content)
        original_name = data.get('siteName')
        
        if original_name and original_name in brand_map:
            data['siteName'] = brand_map[original_name]
            file_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
            print(f"Updated {file_path.name}: {original_name} -> {brand_map[original_name]}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def rebrand_all_sites():
    """Rebrand all 50 sites."""
    print("Starting rebrand of all 50 sites...")
    
    # Process each site folder
    for site_dir in sorted(DEMO_ROOT.glob("*-*")):
        if not site_dir.is_dir():
            continue
        
        print(f"\nProcessing {site_dir.name}...")
        
        # Update HTML files
        html_files = list(site_dir.glob("*.html"))
        html_count = 0
        for html_file in html_files:
            if process_html_file(html_file, BRAND_MAP):
                html_count += 1
        
        # Update site.config.json
        config_file = site_dir / "site.config.json"
        if config_file.exists():
            if process_json_file(config_file, BRAND_MAP):
                pass
        
        # Update site.webmanifest if it exists
        manifest_file = site_dir / "site.webmanifest"
        if manifest_file.exists():
            try:
                content = manifest_file.read_text(encoding='utf-8')
                original = content
                for old_brand, new_brand in BRAND_MAP.items():
                    content = content.replace(old_brand, new_brand)
                if content != original:
                    manifest_file.write_text(content, encoding='utf-8')
            except Exception as e:
                print(f"Error processing {manifest_file}: {e}")
        
        print(f"  Updated {html_count} HTML files")

if __name__ == "__main__":
    rebrand_all_sites()
    print("\n✓ Rebrand complete!")
