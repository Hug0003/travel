#!/usr/bin/env python3
"""
Script pour convertir les images PNG et JPEG en format WebP
Optimise la taille des fichiers tout en conservant une bonne qualité
"""

import os
import sys
from pathlib import Path
from PIL import Image
import argparse

def convert_image_to_webp(input_path, output_path=None, quality=85, optimize=True):
    """
    Convertit un fichier PNG ou JPEG en WebP
    
    Args:
        input_path (str): Chemin vers le fichier image (PNG/JPEG)
        output_path (str, optional): Chemin de sortie. Si None, remplace l'extension
        quality (int): Qualité WebP (1-100, 85 par défaut)
        optimize (bool): Active l'optimisation WebP
    
    Returns:
        str: Chemin du fichier WebP créé
    """
    try:
        # Ouvrir l'image (PNG ou JPEG)
        with Image.open(input_path) as img:
            # Préserver la transparence pour les logos et icônes
            # Seulement convertir en RGB si ce n'est pas un logo
            is_logo = any(keyword in input_path.lower() for keyword in ['logo', 'icon', 'favicon'])
            
            if not is_logo and img.mode in ('RGBA', 'LA'):
                # Créer un fond blanc pour les images avec transparence (photos)
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img, mask=img.split()[-1])
                img = background
            elif img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGB')
            
            # Déterminer le chemin de sortie
            if output_path is None:
                output_path = str(Path(input_path).with_suffix('.webp'))
            
            # Sauvegarder en WebP
            img.save(output_path, 'WebP', quality=quality, optimize=optimize)
            
            # Afficher les informations de compression
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            reduction = ((original_size - new_size) / original_size) * 100
            
            print(f"OK {input_path} -> {output_path}")
            print(f"  Taille: {original_size:,} bytes -> {new_size:,} bytes")
            print(f"  Reduction: {reduction:.1f}%")
            
            return output_path
            
    except Exception as e:
        print(f"ERREUR lors de la conversion de {input_path}: {e}")
        return None

def find_image_files(directory="."):
    """Trouve tous les fichiers PNG et JPEG dans un répertoire et ses sous-répertoires"""
    image_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))
    return image_files

def main():
    parser = argparse.ArgumentParser(description="Convertir les fichiers PNG et JPEG en WebP")
    parser.add_argument("--directory", "-d", default=".", 
                       help="Répertoire à analyser (défaut: répertoire actuel)")
    parser.add_argument("--quality", "-q", type=int, default=85, 
                       help="Qualité WebP 1-100 (défaut: 85)")
    parser.add_argument("--keep-original", "-k", action="store_true",
                       help="Conserver les fichiers originaux")
    parser.add_argument("--files", "-f", nargs="+",
                       help="Fichiers spécifiques à convertir")
    parser.add_argument("--format", choices=['png', 'jpeg', 'all'], default='all',
                       help="Format à convertir (défaut: tous)")
    
    args = parser.parse_args()
    
    # Vérifier que Pillow est installé
    try:
        from PIL import Image
    except ImportError:
        print("ERREUR: La bibliotheque Pillow n'est pas installee.")
        print("Installez-la avec: pip install Pillow")
        sys.exit(1)
    
    print(f"Conversion PNG/JPEG vers WebP (qualite: {args.quality})")
    print("=" * 50)
    
    # Déterminer les fichiers à convertir
    if args.files:
        image_files = args.files
    else:
        all_files = find_image_files(args.directory)
        if args.format == 'png':
            image_files = [f for f in all_files if f.lower().endswith('.png')]
        elif args.format == 'jpeg':
            image_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg'))]
        else:
            image_files = all_files
    
    if not image_files:
        print("AUCUN FICHIER IMAGE TROUVE.")
        return
    
    # Compter par type
    png_count = len([f for f in image_files if f.lower().endswith('.png')])
    jpeg_count = len([f for f in image_files if f.lower().endswith(('.jpg', '.jpeg'))])
    
    print(f"{len(image_files)} fichier(s) image trouve(s)")
    if png_count > 0:
        print(f"   PNG: {png_count}")
    if jpeg_count > 0:
        print(f"   JPEG: {jpeg_count}")
    print()
    
    converted_count = 0
    total_original_size = 0
    total_new_size = 0
    
    for image_file in image_files:
        if os.path.exists(image_file):
            original_size = os.path.getsize(image_file)
            total_original_size += original_size
            
            result = convert_image_to_webp(image_file, quality=args.quality)
            
            if result:
                converted_count += 1
                total_new_size += os.path.getsize(result)
                
                # Supprimer le fichier original si demandé
                if not args.keep_original:
                    try:
                        os.remove(image_file)
                        file_type = "PNG" if image_file.lower().endswith('.png') else "JPEG"
                        print(f"  Fichier {file_type} original supprime")
                    except Exception as e:
                        print(f"  IMPOSSIBLE de supprimer {image_file}: {e}")
            print()
    
    # Résumé final
    if converted_count > 0:
        total_reduction = ((total_original_size - total_new_size) / total_original_size) * 100
        print("=" * 50)
        print(f"CONVERSION TERMINEE!")
        print(f"{converted_count}/{len(image_files)} fichiers convertis")
        print(f"Taille totale: {total_original_size:,} -> {total_new_size:,} bytes")
        print(f"Reduction totale: {total_reduction:.1f}%")
        
        if not args.keep_original:
            print("Fichiers originaux supprimes")
    else:
        print("AUCUN FICHIER n'a pu etre converti.")

if __name__ == "__main__":
    main()
