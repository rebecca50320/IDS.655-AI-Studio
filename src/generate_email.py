#!/usr/bin/env python3
"""
Script to run the digital twin crew and extract only the final email output.
"""

import subprocess
import re
import sys
import os

def run_crew_and_extract_email():
    """Run the crew and extract only the final email output."""
    
    # Change to the correct directory
    os.chdir('/Users/becca/IDS.665/HW1_DigitalTwin/src')
    
    # Run the crew and capture output
    try:
        result = subprocess.run([
            'python3', '-m', 'dad_s_daily_digital_twin.main', 'run'
        ], capture_output=True, text=True, timeout=300)
        
        output = result.stdout
        
        # Extract the final email starting from "TO: dad@example.com"
        email_match = re.search(r'TO: dad@example\.com.*?(?=\n\n|$)', output, re.DOTALL)
        
        if email_match:
            email_content = email_match.group(0)
            
            # Clean up the email content (remove the box drawing characters)
            email_content = re.sub(r'[│└├╭╰─]', '', email_content)
            email_content = re.sub(r'^\s*\|\s*', '', email_content, flags=re.MULTILINE)
            email_content = re.sub(r'\s*\|\s*$', '', email_content, flags=re.MULTILINE)
            email_content = email_content.strip()
            
            # Save to email_output.txt
            with open('email_output.txt', 'w') as f:
                f.write(email_content)
            
            print("✅ Email generated and saved to email_output.txt")
            print("\n" + "="*50)
            print("GENERATED EMAIL:")
            print("="*50)
            print(email_content)
            
        else:
            print("❌ Could not find email in crew output")
            print("Raw output preview:")
            print(output[-1000:])  # Show last 1000 characters
            
    except subprocess.TimeoutExpired:
        print("❌ Crew execution timed out")
    except Exception as e:
        print(f"❌ Error running crew: {e}")

if __name__ == "__main__":
    run_crew_and_extract_email()
