CATEGORY_FALLBACK_IMAGES = {
    "electronics": "https://images.unsplash.com/photo-1544731612-de292439cc67?auto=format&fit=crop&w=900&q=80",
    "laptops": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80",
    "smartphones": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80",
    "headphones": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80",
    "monitors": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=900&q=80",
    "fashion": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=900&q=80",
    "footwear": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
    "accessories": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=900&q=80",
    "home & lifestyle": "https://images.unsplash.com/photo-1534353436294-0dbd4bdac845?auto=format&fit=crop&w=900&q=80",
    "gifts": "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&w=900&q=80"
}

def get_image_with_fallback(image_url: str, category: str = "electronics") -> str:
    if not image_url or image_url.startswith("/placeholder") or image_url == "":
        cat_key = category.lower()
        return CATEGORY_FALLBACK_IMAGES.get(cat_key, CATEGORY_FALLBACK_IMAGES["electronics"])
    return image_url
