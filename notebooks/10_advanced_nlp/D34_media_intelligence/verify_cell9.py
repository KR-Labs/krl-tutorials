"""
Verification script to confirm Cell 9 executed properly
Run this AFTER executing cells 0-9 in the notebook
"""

def verify_cell9_execution():
    """Check if df_enriched was created successfully"""

    print("="*80)
    print("CELL 9 EXECUTION VERIFICATION")
    print("="*80)

    # Check if df_enriched exists
    try:
        if 'df_enriched' in globals():
            print(f"\n✅ df_enriched EXISTS in global scope")
            print(f"   Type: {type(df_enriched)}")
            print(f"   Shape: {df_enriched.shape}")
            print(f"   Columns: {list(df_enriched.columns)}")

            # Check for key columns
            required_cols = ['full_text', 'text_for_clustering', 'extraction_method']
            missing = [col for col in required_cols if col not in df_enriched.columns]

            if missing:
                print(f"\n⚠️  Missing columns: {missing}")
            else:
                print(f"\n✅ All required columns present")

            # Check enrichment success
            if 'extraction_method' in df_enriched.columns:
                method_counts = df_enriched['extraction_method'].value_counts()
                print(f"\n📊 Enrichment Methods:")
                for method, count in method_counts.items():
                    pct = count / len(df_enriched) * 100
                    print(f"   • {method}: {count} ({pct:.1f}%)")

            print(f"\n✅ PHASE 1 COMPLETE: Cell 9 executed successfully!")
            print(f"   You can now proceed to run cells 10-13")
            return True
        else:
            print(f"\n❌ df_enriched DOES NOT EXIST")
            print(f"\n🔧 Solution:")
            print(f"   1. Restart kernel")
            print(f"   2. Run cells 0-9 in order")
            print(f"   3. Wait for cell 9 to complete (5-8 minutes)")
            return False

    except Exception as e:
        print(f"\n❌ Error checking df_enriched: {e}")
        return False

if __name__ == "__main__":
    verify_cell9_execution()
