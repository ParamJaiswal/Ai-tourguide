"""Setup script to install spaCy model and dependencies."""

import subprocess
import sys


def install_spacy_model():
    """Install spaCy English model."""
    print("Installing spaCy English model...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "spacy", "download", "en_core_web_sm"
        ])
        print("✓ Successfully installed spaCy model: en_core_web_sm")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install spaCy model: {e}")
        return False


def verify_installation():
    """Verify spaCy installation."""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✓ spaCy model verified successfully")
        return True
    except Exception as e:
        print(f"✗ Verification failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Inkle Tourism System - NLP Setup")
    print("=" * 60)
    print()
    
    # Install model
    if install_spacy_model():
        print()
        # Verify
        if verify_installation():
            print()
            print("=" * 60)
            print("Setup complete! You can now run the application.")
            print("=" * 60)
        else:
            sys.exit(1)
    else:
        sys.exit(1)
