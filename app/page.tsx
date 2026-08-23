'use client'

import { useMemo, useState } from 'react'
import Link from 'next/link'
import { ArrowRight, Check, ChevronDown, Heart, Menu, MessageCircle, ShoppingCart, Sparkles, Star, X } from 'lucide-react'
import { Logo } from '@/components/logo'

type Product = { id: string; name: string; category: string; price: number; oldPrice?: number; rating: number; reviews: number; image: string; badge?: string; specs: string[] }

const products: Product[] = [
  { id: 'aero-buds-pro', name: 'AeroBuds Pro', category: 'Audio', price: 4499, oldPrice: 5999, rating: 4.7, reviews: 1284, image: 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=900&q=85', badge: 'Best match', specs: ['Active noise cancellation', '32 hr battery', 'IPX4'] },
  { id: 'sonic-beam', name: 'SonicBeam Wireless', category: 'Audio', price: 3299, oldPrice: 3999, rating: 4.5, reviews: 892, image: 'https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?auto=format&fit=crop&w=900&q=85', specs: ['Hybrid ANC', '40 hr battery', 'Multipoint'] },
  { id: 'pixelview-27', name: 'PixelView 27 4K', category: 'Monitors', price: 28999, oldPrice: 33999, rating: 4.8, reviews: 456, image: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=900&q=85', badge: 'Top rated', specs: ['4K UHD', '144Hz refresh', 'USB-C 90W'] },
  { id: 'zenbook-air', name: 'ZenBook Air 14', category: 'Laptops', price: 74999, oldPrice: 82999, rating: 4.6, reviews: 671, image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85', specs: ['Intel Core Ultra 5', '16GB RAM', '512GB SSD'] },
]

const money = (n: number) => `₹${n.toLocaleString('en-IN')}`

export default function Page() {
  const [query, setQuery] = useState('')
  const [language, setLanguage] = useState('EN')
  const [menuOpen, setMenuOpen] = useState(false)
  const [cart, setCart] = useState<Product[]>([])
  const [wishlisted, setWishlisted] = useState<string[]>([])
  const [prompt, setPrompt] = useState('')
  const [asked, setAsked] = useState(false)
  const [toast, setToast] = useState('')

  const results = useMemo(() => products.filter((p) => !query || `${p.name} ${p.category}`.toLowerCase().includes(query.toLowerCase())), [query])
  const addToCart = (product: Product) => { setCart((current) => current.some((p) => p.id === product.id) ? current : [...current, product]); setToast(`${product.name} added to cart`); setTimeout(() => setToast(''), 2200) }
  const submitPrompt = (value = prompt) => { setPrompt(value); setAsked(true) }

  return (
    <main className="min-h-screen bg-background text-foreground">
      {toast && <div className="toast" role="status"><Check size={16} />{toast}</div>}
      <header className="site-header">
        <div className="header-inner">
          <Link href="/" aria-label="SmartCart Home">
            <Logo size="md" />
          </Link>
          <nav className="desktop-nav" aria-label="Main navigation"><Link className="active" href="/">Home</Link><Link href="#recommendations">Explore</Link><Link href="#compare">Compare</Link><Link href="#orders">Orders</Link></nav>
          <div className="header-actions"><button className="language" onClick={() => setLanguage(language === 'EN' ? 'TE' : 'EN')} aria-label="Change language">{language} <ChevronDown size={14} /></button><Link href="#cart" className="cart-link" aria-label="Cart"><ShoppingCart size={19} /><span>{cart.length}</span></Link><button className="menu-button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Open menu">{menuOpen ? <X /> : <Menu />}</button></div>
        </div>
        {menuOpen && <nav className="mobile-nav"><Link href="#recommendations" onClick={() => setMenuOpen(false)}>Explore products</Link><Link href="#compare" onClick={() => setMenuOpen(false)}>Compare</Link><Link href="#orders" onClick={() => setMenuOpen(false)}>Orders</Link></nav>}
      </header>

      <section className="hero-shell">
        <div className="hero-copy"><div className="eyebrow"><span className="pulse-dot" /> Shopping, simplified</div><h1>Your smarter way to shop.</h1><p>Tell us what you need. SmartCart finds the best products for your budget, use case, and preferences.</p><div className="hero-links"><Link href="#recommendations">Browse products <ArrowRight size={15} /></Link><Link href="#how-it-works">How it works</Link></div></div>
        <div className="assistant-card"><div className="assistant-top"><div className="assistant-title"><span className="sparkle-icon"><Sparkles size={16} /></span><div><strong>Ask SmartCart</strong><small>Your personal shopping assistant</small></div></div><span className="online"><span /> Online</span></div><div className="assistant-body"><label htmlFor="shopping-prompt">What are you looking for?</label><div className="prompt-box"><textarea id="shopping-prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="e.g. Best earbuds under ₹5,000 for calls..." rows={2} /><button onClick={() => submitPrompt()} aria-label="Ask SmartCart"><ArrowRight size={18} /></button></div><div className="prompt-examples"><button onClick={() => submitPrompt('Best earbuds under ₹5,000 for calls')}>Best earbuds under ₹5,000</button><button onClick={() => submitPrompt('Monitor for my home office')}>Monitor for home office</button></div>{asked && <div className="assistant-answer"><div className="answer-head"><Sparkles size={15} /> SmartCart recommends</div><p>Based on “{prompt}”, I found {results.length || 2} strong matches from our catalogue.</p><Link href="#recommendations">See recommendations <ArrowRight size={14} /></Link></div>}</div></div>
      </section>

      <section className="trust-row"><div><Check size={17} /> Unbiased recommendations</div><div><Check size={17} /> Compare prices easily</div><div><Check size={17} /> Shop with confidence</div></section>

      <section className="section" id="recommendations"><div className="section-heading"><div><span className="section-kicker">CURATED FOR YOU</span><h2>Popular right now</h2><p>Top picks, handpicked by SmartCart.</p></div><Link href="#all-products" className="text-link">View all products <ArrowRight size={15} /></Link></div><div className="product-grid">{results.slice(0, 4).map((product) => <ProductCard key={product.id} product={product} wished={wishlisted.includes(product.id)} onWish={() => setWishlisted((w) => w.includes(product.id) ? w.filter((id) => id !== product.id) : [...w, product.id])} onAdd={() => addToCart(product)} />)}</div></section>

      <section className="how-section" id="how-it-works"><div className="section-heading centered"><span className="section-kicker">HOW IT WORKS</span><h2>Shopping, but smarter.</h2><p>From question to checkout in three simple steps.</p></div><div className="steps"><div className="step"><span>01</span><div className="step-icon"><MessageCircle size={21} /></div><h3>Tell us what you need</h3><p>Ask in your own words, in English or Telugu.</p></div><div className="step-line" /><div className="step"><span>02</span><div className="step-icon"><Sparkles size={21} /></div><h3>Get smart recommendations</h3><p>We match your needs with the best available products.</p></div><div className="step-line" /><div className="step"><span>03</span><div className="step-icon"><ShoppingCart size={21} /></div><h3>Choose with confidence</h3><p>Compare, save favorites, and checkout when ready.</p></div></div></section>

      <section className="category-section" id="all-products"><div className="section-heading"><div><span className="section-kicker">EXPLORE CATEGORIES</span><h2>Find your next favorite.</h2></div></div><div className="category-grid"><Link href="#recommendations" className="category-card category-audio"><span>Audio</span><small>Earbuds, headphones & more <ArrowRight size={14} /></small></Link><Link href="#recommendations" className="category-card category-work"><span>Work essentials</span><small>Monitors, laptops & accessories <ArrowRight size={14} /></small></Link><Link href="#recommendations" className="category-card category-home"><span>Home & living</span><small>Make your space better <ArrowRight size={14} /></small></Link></div></section>

      <section className="newsletter"><div><span className="section-kicker">STAY IN THE LOOP</span><h2>Smarter finds, straight to your inbox.</h2><p>Weekly picks, price drops, and shopping tips. No spam, ever.</p></div><form onSubmit={(e) => e.preventDefault()}><input type="email" placeholder="Your email address" aria-label="Email address" /><button>Subscribe</button></form></section>
      <footer>
        <Link href="/" aria-label="SmartCart Home">
          <Logo size="sm" />
        </Link>
        <span>Made for better decisions.</span>
        <div><Link href="#compare">Compare</Link><Link href="#orders">Orders</Link><Link href="#cart">Cart ({cart.length})</Link></div>
      </footer>
    </main>
  )
}

function ProductCard({ product, wished, onWish, onAdd }: { product: Product; wished: boolean; onWish: () => void; onAdd: () => void }) {
  return <article className="product-card"><div className="product-image-wrap"><img src={product.image} alt={product.name} className="product-image" /><button className={`wish-button ${wished ? 'wished' : ''}`} onClick={onWish} aria-label={`Save ${product.name}`}><Heart size={18} fill={wished ? 'currentColor' : 'none'} /></button>{product.badge && <span className="product-badge">{product.badge}</span>}</div><div className="product-info"><span className="product-category">{product.category}</span><h3>{product.name}</h3><div className="rating"><Star size={14} fill="currentColor" /> {product.rating} <span>({product.reviews.toLocaleString()})</span></div><div className="price-row"><strong>{money(product.price)}</strong>{product.oldPrice && <del>{money(product.oldPrice)}</del>}</div><button className="add-button" onClick={onAdd}>Add to cart <ArrowRight size={15} /></button></div></article>
}

