#!/usr/bin/env python3
"""
================================================================================
 Touch Grass to Deploy - Git Pre-Push Gatekeeper
 DEV Community x Hugging Face Hacktoberfest Challenge ("Touch Grass" Theme)
================================================================================
 This script intercepts git push attempts and verifies that the developer has
 taken physical proof of real outdoor nature before deploying their code.

 Powered by open-weight local vision-language model: vikhyatk/moondream2
 - Runs completely on CPU with zero cloud dependencies
 - 100% offline, privacy-safe, and free forever
================================================================================
"""

import sys
import os
import argparse
from pathlib import Path

# ANSI color codes for terminal formatting
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    DIM = "\033[2m"

def print_banner():
    banner = f"""
{Colors.GREEN}{Colors.BOLD}======================================================================
  🌿 TOUCH GRASS TO DEPLOY | Git Pre-Push Gatekeeper 🌿
  Dev Community x Hugging Face Hacktoberfest Challenge
======================================================================{Colors.RESET}"""
    print(banner)

def find_grass_image(repo_root: Path, custom_path: str = None) -> Path:
    """Find a grass/nature proof image in working directory or repo root."""
    if custom_path:
        p = Path(custom_path)
        if p.is_file():
            return p
        return None

    supported_extensions = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG"]
    
    # Check current working directory first, then repository root
    search_dirs = [Path.cwd()]
    if repo_root not in search_dirs:
        search_dirs.append(repo_root)

    for directory in search_dirs:
        for ext in supported_extensions:
            candidate = directory / f"grass{ext}"
            if candidate.is_file():
                return candidate

    return None

def verify_nature_with_moondream(image_path: Path) -> tuple[bool, str]:
    """
    Load the open-weight moondream2 model locally and verify if the image
    depicts real outdoor nature, grass, plants, foliage, or sky.
    """
    print(f"\n{Colors.CYAN}[1/3] 📷 Inspecting proof: {image_path.name}...{Colors.RESET}")
    
    try:
        from PIL import Image
    except ImportError:
        print(f"{Colors.RED}❌ Error: Pillow is not installed. Run: pip install -r requirements.txt{Colors.RESET}")
        return False, "Pillow library missing."

    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: Unable to open image file '{image_path}': {e}{Colors.RESET}")
        return False, f"Corrupted or invalid image: {e}"

    print(f"{Colors.CYAN}[2/3] 🧠 Initializing local vision model (vikhyatk/moondream2 on CPU)...{Colors.RESET}")
    print(f"{Colors.DIM}      (Zero cloud API calls. Complete offline privacy.){Colors.RESET}")

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError:
        print(f"{Colors.RED}❌ Error: PyTorch or Transformers not installed. Run: pip install -r requirements.txt{Colors.RESET}")
        return False, "Missing deep learning dependencies."

    model_id = "vikhyatk/moondream2"
    revision = "2024-08-26"

    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            trust_remote_code=True,
            revision=revision,
            low_cpu_mem_usage=True,
        )
        tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        model.eval()
    except Exception as e:
        print(f"{Colors.RED}❌ Error loading local model '{model_id}': {e}{Colors.RESET}")
        return False, f"Model initialization failed: {e}"

    print(f"{Colors.CYAN}[3/3] 🔍 Analyzing visual features for authentic outdoor nature...{Colors.RESET}")
    prompt = "Is this image showing real outdoor nature, plants, grass, trees, or sky? Answer only YES or NO."

    try:
        with torch.no_grad():
            image_embeds = model.encode_image(image)
            answer = model.answer_question(image_embeds, prompt, tokenizer)
    except Exception as e:
        print(f"{Colors.RED}❌ Error during visual inference: {e}{Colors.RESET}")
        return False, f"Inference failed: {e}"

    cleaned_answer = answer.strip().upper()
    print(f"{Colors.DIM}      AI Model Verdict: {cleaned_answer}{Colors.RESET}")

    if cleaned_answer.startswith("YES") or "YES" in cleaned_answer:
        return True, cleaned_answer
    else:
        return False, cleaned_answer

def main():
    parser = argparse.ArgumentParser(
        description="Touch Grass to Deploy: Pre-Push Nature Verification"
    )
    parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="Optional custom path to the proof image",
    )
    parser.add_argument(
        "--keep-image",
        action="store_true",
        help="Keep the proof image instead of deleting it after successful verification",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform verification without exiting with failure code or deleting image",
    )
    args = parser.parse_args()

    print_banner()

    repo_root = Path(__file__).resolve().parent
    image_path = find_grass_image(repo_root, args.image)

    if not image_path:
        print(f"""
{Colors.RED}{Colors.BOLD}🚫 DEPLOYMENT BLOCKED: NO PROOF OF NATURE FOUND!{Colors.RESET}
----------------------------------------------------------------------
You have attempted to `git push` without providing physical evidence
that you have stepped away from your screen.

{Colors.YELLOW}{Colors.BOLD}👉 HOW TO UNLOCK YOUR GIT PUSH:{Colors.RESET}
  1. Stand up from your desk.
  2. Walk outside into the physical world.
  3. Touch real grass, foliage, or gaze at the sky.
  4. Snap a photo on your phone.
  5. Save the photo as {Colors.BOLD}grass.jpg{Colors.RESET} in your project root:
     {Colors.CYAN}{Path.cwd() / 'grass.jpg'}{Colors.RESET}
  6. Re-run {Colors.BOLD}`git push`{Colors.RESET}.

{Colors.DIM}"The screen should be the shortest part of the experience."{Colors.RESET}
----------------------------------------------------------------------
""")
        sys.exit(0 if args.dry_run else 1)

    print(f"{Colors.YELLOW}Found candidate proof: {image_path.name}{Colors.RESET}")
    is_nature, raw_response = verify_nature_with_moondream(image_path)

    if is_nature:
        print(f"""
{Colors.GREEN}{Colors.BOLD}✅ PROOF ACCEPTED! NATURE CONFIRMED.{Colors.RESET}
----------------------------------------------------------------------
🌿 Congratulations! You touched grass and disconnected from the matrix.
🚀 Your git push has been authorized by local vision intelligence.
""")
        if not args.keep_image and not args.dry_run:
            try:
                os.remove(image_path)
                print(f"{Colors.DIM}🧹 Consumed {image_path.name} (fresh proof required for future pushes).{Colors.RESET}\n")
            except Exception as e:
                print(f"{Colors.YELLOW}⚠️  Could not remove {image_path.name}: {e}{Colors.RESET}\n")

        print(f"{Colors.GREEN}Proceeding with remote deployment...{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"""
{Colors.RED}{Colors.BOLD}🚫 REJECTED: THIS DOES NOT LOOK LIKE REAL NATURE!{Colors.RESET}
----------------------------------------------------------------------
Model response: {raw_response}

The local vision AI determined this image does NOT show authentic
outdoor nature, grass, plants, trees, or sky.

Please do not submit screenshots of code, indoor monitors, wallpapers,
or artificial renders. Go outside, touch real grass, take an authentic
photo, save it as {Colors.BOLD}grass.jpg{Colors.RESET}, and re-run `git push`.
----------------------------------------------------------------------
""")
        sys.exit(0 if args.dry_run else 1)

if __name__ == "__main__":
    main()
