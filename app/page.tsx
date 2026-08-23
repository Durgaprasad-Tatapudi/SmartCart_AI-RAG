'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'
import {
  ArrowRight,
  Bell,
  Check,
  ChevronDown,
  Heart,
  Menu,
  MessageCircle,
  Package,
  Plus,
  Minus,
  Scale,
  ShoppingCart,
  Sparkles,
  Star,
  Trash2,
  X
} from 'lucide-react'
import { Logo } from '@/components/logo'
import { api, Product, AssistantResponse, CartResponse, Order } from '@/lib/api'

const initialProducts: Product[] = [
  { id: 'aero-buds-pro', name: 'AeroBuds Pro', category: 'Audio', price: 4499, oldPrice: 5999, rating: 4.7, reviews: 1284, image: 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=900&q=85', badge: 'Best match', specs: ['Active noise cancellation', '32 hr battery', 'IPX4'] },
  { id: 'sonic-beam', name: 'SonicBeam Wireless', category: 'Audio', price: 3299, oldPrice: 3999, rating: 4.5, reviews: 892, image: 'https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?auto=format&fit=crop&w=900&q=85', specs: ['Hybrid ANC', '40 hr battery', 'Multipoint'] },
  { id: 'pixelview-27', name: 'PixelView 27 4K', category: 'Monitors', price: 28999, oldPrice: 33999, rating: 4.8, reviews: 456, image: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=900&q=85', badge: 'Top rated', specs: ['4K UHD', '144Hz refresh', 'USB-C 90W'] },
  { id: 'zenbook-air', name: 'ZenBook Air 14', category: 'Laptops', price: 74999, oldPrice: 82999, rating: 4.6, reviews: 671, image: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85', specs: ['Intel Core Ultra 5', '16GB RAM', '512GB SSD'] },
]

const money = (n: number) => `₹${n.toLocaleString('en-IN')}`

export default function Page() {
  const [query, setQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState<string>('all')
  const [language, setLanguage] = useState<'EN' | 'TE'>('EN')
  const [menuOpen, setMenuOpen] = useState(false)
  const [cartOpen, setCartOpen] = useState(false)
  const [compareOpen, setCompareOpen] = useState(false)
  const [ordersOpen, setOrdersOpen] = useState(false)
  const [checkoutStep, setCheckoutStep] = useState(false)

  // Data states
  const [cartData, setCartData] = useState<CartResponse | null>(null)
  const [compareList, setCompareList] = useState<Product[]>([])
  const [compareExplanation, setCompareExplanation] = useState<string>('')
  const [isComparing, setIsComparing] = useState(false)
  const [ordersList, setOrdersList] = useState<Order[]>([])
  const [wishlisted, setWishlisted] = useState<string[]>([])
  const [prompt, setPrompt] = useState('')
  const [asked, setAsked] = useState(false)
  const [isThinking, setIsThinking] = useState(false)
  const [aiResponse, setAiResponse] = useState<AssistantResponse | null>(null)
  const [toast, setToast] = useState('')
  const [catalogProducts, setCatalogProducts] = useState<Product[]>(initialProducts)

  // Subscription / Alert state
  const [subscribing, setSubscribing] = useState(false)
  const [subEmail, setSubEmail] = useState('')
  const [subscribedCategory, setSubscribedCategory] = useState<string | null>(null)

  const handleSubscribe = async (offer: any) => {
    if (!offer) return
    setSubscribing(true)
    try {
      const res = await api.subscribe({
        email: subEmail || undefined,
        category: offer.category || 'General',
        max_price: offer.max_price,
        language: language === 'TE' ? 'telugu' : 'english'
      })
      setSubscribing(false)
      if (res?.success) {
        setSubscribedCategory(offer.category)
        setToast(res.message)
        setTimeout(() => setToast(''), 3500)
      } else {
        setToast(res?.message || 'Subscription failed')
        setTimeout(() => setToast(''), 2500)
      }
    } catch (err) {
      setSubscribing(false)
      setToast('Subscription service unavailable')
      setTimeout(() => setToast(''), 2500)
    }
  }

  // Checkout address state
  const [shippingAddress, setShippingAddress] = useState({
    full_name: 'Ravi Kumar',
    phone: '+91 9876543210',
    address_line: 'Flat 402, High Tech City',
    city: 'Hyderabad',
    state: 'Telangana',
    pincode: '500081'
  })
  const [paymentMethod, setPaymentMethod] = useState('UPI')

  const [activeSearchQuery, setActiveSearchQuery] = useState('')
  const [initialCatalog, setInitialCatalog] = useState<Product[]>([])

  // Load products & session data from backend on mount
  useEffect(() => {
    async function loadInitialData() {
      const data = await api.getProducts({ limit: 40 })
      if (data?.products && data.products.length > 0) {
        setCatalogProducts(data.products)
        setInitialCatalog(data.products)
      }
      
      const cartResp = await api.getCart()
      if (cartResp) {
        setCartData(cartResp)
      }

      const wishData = await api.getWishlist()
      if (wishData && wishData.length > 0) {
        setWishlisted(wishData.map((p) => p.id))
      }
    }
    loadInitialData()
  }, [])

  // Filter products based on search or category
  const results = useMemo(() => {
    let list = catalogProducts
    if (selectedCategory && selectedCategory !== 'all') {
      list = list.filter((p) => 
        p.category.toLowerCase() === selectedCategory.toLowerCase() || 
        p.subcategory?.toLowerCase() === selectedCategory.toLowerCase()
      )
    }
    if (query.trim()) {
      const q = query.toLowerCase()
      list = list.filter((p) => 
        `${p.name} ${p.category} ${p.brand || ''} ${p.specs.join(' ')}`.toLowerCase().includes(q)
      )
    }
    return list
  }, [catalogProducts, selectedCategory, query])

  const totalCartCount = useMemo(() => {
    return cartData?.item_count || 0
  }, [cartData])

  const addToCart = async (product: Product) => {
    const updated = await api.addToCart(product.id, 1)
    if (updated) setCartData(updated)
    setToast(`${product.name} added to cart`)
    setTimeout(() => setToast(''), 2200)
  }

  const updateCartQty = async (productId: string, quantity: number) => {
    const updated = await api.updateCartItem(productId, quantity)
    if (updated) setCartData(updated)
  }

  const removeCartItem = async (productId: string) => {
    const updated = await api.removeFromCart(productId)
    if (updated) setCartData(updated)
  }

  const toggleWishlist = async (productId: string) => {
    setWishlisted((w) => w.includes(productId) ? w.filter((id) => id !== productId) : [...w, productId])
    await api.toggleWishlist(productId)
  }

  const toggleCompare = (product: Product) => {
    setCompareList((prev) => {
      const exists = prev.some((p) => p.id === product.id)
      if (exists) {
        return prev.filter((p) => p.id !== product.id)
      } else {
        if (prev.length >= 4) {
          setToast('You can compare maximum 4 products at once')
          setTimeout(() => setToast(''), 2500)
        } else {
          setToast(`Added ${product.name} to comparison`)
          setTimeout(() => setToast(''), 2200)
        }
        return [...prev, product]
      }
    })
  }

  const runAiCompare = async () => {
    if (compareList.length < 2) return
    setIsComparing(true)
    try {
      const resp = await api.getComparisonInsights(compareList.map((p) => p.id), undefined, language)
      setIsComparing(false)
      if (resp?.explanation) {
        setCompareExplanation(resp.explanation)
      } else if (resp?.comparison) {
        setCompareExplanation(
          `Compared ${compareList.map((p) => p.name).join(' vs ')} based on live specifications, pricing, and ratings.`
        )
      }
    } catch (err) {
      setIsComparing(false)
      console.error('Comparison error:', err)
    }
  }

  const openOrdersModal = async () => {
    setOrdersOpen(true)
    const orders = await api.getOrders()
    if (orders) setOrdersList(orders)
  }

  const handlePlaceOrder = async () => {
    if (!cartData || cartData.items.length === 0) return
    const order = await api.placeOrder(shippingAddress, paymentMethod)
    if (order) {
      setToast('Order placed successfully! (Demo Mode)')
      setCheckoutStep(false)
      setCartOpen(false)
      setCartData(null)
      openOrdersModal()
    }
  }

  const handleExplore = (e?: React.MouseEvent) => {
    if (e) e.preventDefault()
    setActiveSearchQuery('')
    setSelectedCategory('all')
    setCompareOpen(false)
    setOrdersOpen(false)
    if (initialCatalog.length > 0) setCatalogProducts(initialCatalog)
    setTimeout(() => {
      document.getElementById('recommendations')?.scrollIntoView({ behavior: 'smooth' })
    }, 50)
  }

  const scrollToRecommendations = (e?: React.MouseEvent) => {
    if (e) e.preventDefault()
    document.getElementById('recommendations')?.scrollIntoView({ behavior: 'smooth' })
  }

  const toggleLanguage = () => {
    const next = language === 'EN' ? 'TE' : 'EN'
    setLanguage(next)
    setToast(next === 'TE' ? 'భాష తెలుగుకి మార్చబడింది (Telugu)' : 'Language switched to English')
    setTimeout(() => setToast(''), 2200)
  }

  const submitPrompt = async (value = prompt) => {
    if (!value.trim()) return
    setPrompt(value)
    setActiveSearchQuery(value)
    setAsked(true)
    setIsThinking(true)
    
    try {
      const resp = await api.askAssistant(value, [], language)
      setIsThinking(false)
      if (resp) {
        setAiResponse(resp)
        if (resp.products && resp.products.length > 0) {
          setSelectedCategory('all')
          setCatalogProducts(resp.products)
          // Automatically bring recommendations into view immediately
          setTimeout(() => {
            document.getElementById('recommendations')?.scrollIntoView({ behavior: 'smooth' })
          }, 150)
        }
      }
    } catch (err) {
      setIsThinking(false)
      console.error('Submit prompt error:', err)
    }
  }

  const filterByCategory = (categoryName: string) => {
    setActiveSearchQuery('')
    setSelectedCategory(categoryName)
    if (initialCatalog.length > 0) setCatalogProducts(initialCatalog)
    setTimeout(() => {
      document.getElementById('recommendations')?.scrollIntoView({ behavior: 'smooth' })
    }, 50)
  }

  return (
    <main className="min-h-screen bg-background text-foreground">
      {toast && <div className="toast" role="status"><Check size={16} />{toast}</div>}
      
      {/* Header */}
      <header className="site-header">
        <div className="header-inner">
          <Link href="/" aria-label="SmartCart Home" onClick={() => setSelectedCategory('all')}>
            <Logo size="md" />
          </Link>
          <nav className="desktop-nav" aria-label="Main navigation">
            <button 
              className={`nav-link ${selectedCategory === 'all' && !compareOpen && !ordersOpen && !activeSearchQuery ? 'active' : ''}`}
              onClick={() => { setSelectedCategory('all'); setActiveSearchQuery(''); setCompareOpen(false); setOrdersOpen(false); }}
            >
              {language === 'TE' ? 'హోమ్' : 'Home'}
            </button>
            <button
              onClick={handleExplore}
              className={`nav-link ${selectedCategory !== 'all' || activeSearchQuery ? 'active' : ''}`}
            >
              {language === 'TE' ? 'అన్వేషించండి' : 'Explore'}
            </button>
            <button 
              className={`nav-link ${compareOpen ? 'active' : ''}`}
              onClick={() => setCompareOpen(true)}
            >
              {language === 'TE' ? 'పోల్చండి' : 'Compare'} {compareList.length > 0 && `(${compareList.length})`}
            </button>
            <button 
              className={`nav-link ${ordersOpen ? 'active' : ''}`}
              onClick={openOrdersModal}
            >
              {language === 'TE' ? 'ఆర్డర్లు' : 'Orders'}
            </button>
          </nav>
          <div className="header-actions">
            <button className="language" onClick={toggleLanguage} aria-label="Change language" style={{ background: 'var(--accent)', padding: '6px 10px', borderRadius: '6px', color: 'var(--primary)' }}>
              {language === 'EN' ? '🇬🇧 English' : '🇮🇳 తెలుగు'} <ChevronDown size={14} />
            </button>
            <button onClick={() => setCartOpen(true)} className="cart-link" aria-label="Cart">
              <ShoppingCart size={19} />
              <span>{totalCartCount}</span>
            </button>
            <button className="menu-button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Open menu">
              {menuOpen ? <X /> : <Menu />}
            </button>
          </div>
        </div>
        {menuOpen && (
          <nav className="mobile-nav">
            <button onClick={() => { handleExplore(); setMenuOpen(false); }} style={{ textAlign: 'left', padding: '6px 0', background: 'none', border: 'none', cursor: 'pointer' }}>
              {language === 'TE' ? 'అన్వేషించండి' : 'Explore products'}
            </button>
            <button className="language" style={{ textAlign: 'left', padding: '6px 0' }} onClick={() => { setCompareOpen(true); setMenuOpen(false) }}>
              {language === 'TE' ? 'పోల్చండి' : 'Compare'} {compareList.length > 0 && `(${compareList.length})`}
            </button>
            <button className="language" style={{ textAlign: 'left', padding: '6px 0' }} onClick={() => { openOrdersModal(); setMenuOpen(false) }}>
              {language === 'TE' ? 'ఆర్డర్లు' : 'Orders'}
            </button>
          </nav>
        )}
      </header>

      {/* Hero Section */}
      <section className="hero-shell">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="pulse-dot" /> {language === 'TE' ? 'షాపింగ్, మరింత సులభం' : 'Shopping, simplified'}
          </div>
          <h1>{language === 'TE' ? 'షాపింగ్ చేయడానికి మీ స్మార్ట్ మార్గం.' : 'Your smarter way to shop.'}</h1>
          <p>
            {language === 'TE' 
              ? 'మీకు ఏమి కావాలో మాకు చెప్పండి. మీ బడ్జెట్, ఉపయోగం మరియు ప్రాధాన్యతలకు సరిపోయే ఉత్తమ ఉత్పత్తులను SmartCart వెతుకుతుంది.'
              : 'Tell us what you need. SmartCart finds the best products for your budget, use case, and preferences.'}
          </p>
          <div className="hero-links">
            <button onClick={handleExplore} style={{ background: 'none', border: 'none', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '7px', color: 'var(--primary)', fontWeight: 700, fontSize: '13px' }}>
              {language === 'TE' ? 'ఉత్పత్తులను చూడండి' : 'Browse products'} <ArrowRight size={15} />
            </button>
            <Link href="#how-it-works">{language === 'TE' ? 'ఇది ఎలా పనిచేస్తుంది' : 'How it works'}</Link>
          </div>
        </div>
        
        <div className="assistant-card">
          <div className="assistant-top">
            <div className="assistant-title">
              <span className="sparkle-icon"><Sparkles size={16} /></span>
              <div>
                <strong>{language === 'TE' ? 'SmartCart ని అడగండి' : 'Ask SmartCart'}</strong>
                <small>{language === 'TE' ? 'మీ వ్యక్తిగత బహుభాషా షాపింగ్ అసిస్టెంట్' : 'Your multilingual shopping assistant'}</small>
              </div>
            </div>
            <span className="online"><span /> Online</span>
          </div>
          <div className="assistant-body">
            <label htmlFor="shopping-prompt">
              {language === 'TE' ? 'మీరు దేని కోసం వెతుకుతున్నారు?' : 'What are you looking for?'}
            </label>
            <div className="prompt-box">
              <textarea
                id="shopping-prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    submitPrompt()
                  }
                }}
                placeholder={
                  language === 'TE'
                    ? 'ఉదా: ₹5,000 లోపు మంచి ఇయర్‌బడ్స్, లేదా 60k lopu coding laptop...'
                    : 'e.g. Best earbuds under ₹5,000, or laptop for coding...'
                }
                rows={2}
              />
              <button onClick={() => submitPrompt()} aria-label="Ask SmartCart" disabled={isThinking}>
                <ArrowRight size={18} />
              </button>
            </div>
            
            <div className="prompt-examples">
              {language === 'TE' ? (
                <>
                  <button onClick={() => submitPrompt('Naku 60k lopu coding laptop kavali')}>60k లోపు coding laptop</button>
                  <button onClick={() => submitPrompt('Best earbuds under ₹5,000 for calls')}>₹5,000 లోపు earbuds</button>
                  <button onClick={() => submitPrompt('నాకు మంచి running shoes కావాలి')}>Running shoes</button>
                </>
              ) : (
                <>
                  <button onClick={() => submitPrompt('Best earbuds under ₹5,000 for calls')}>Best earbuds under ₹5,000</button>
                  <button onClick={() => submitPrompt('Laptop for coding under 60000')}>Coding laptop under ₹60k</button>
                  <button onClick={() => submitPrompt('Monitor for my home office')}>Monitor for home office</button>
                </>
              )}
            </div>

            {asked && (
              <div className="assistant-answer">
                <div className="answer-head">
                  <Sparkles size={15} /> {isThinking ? (language === 'TE' ? 'SmartCart వెతుకుతోంది...' : 'SmartCart is searching catalogue...') : (language === 'TE' ? 'SmartCart సిఫార్సు చేస్తోంది' : 'SmartCart recommends')}
                </div>
                <p style={{ lineHeight: 1.55, fontSize: '13px', whiteSpace: 'pre-line' }}>
                  {isThinking
                    ? (language === 'TE' ? 'మీ అభ్యర్థనను విశ్లేషించి, సరైన వెక్టర్స్ మరియు ధరలను సరిపోలుస్తోంది...' : 'Understanding your request, finding best matching vectors, and checking prices...')
                    : aiResponse?.message || `Based on “${prompt}”, I found ${results.length || 4} strong matches from our catalogue.`}
                </p>

                {/* Render Direct Match Products */}
                {!isThinking && (aiResponse?.exact_matches?.length ?? 0) > 0 && (
                  <div style={{ marginTop: '14px', borderTop: '1px solid rgba(20, 93, 79, 0.15)', paddingTop: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                      <strong style={{ fontSize: '12px', color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '5px' }}>
                        <Sparkles size={13} /> {language === 'TE' ? 'మీకు సరిపోయే ఎంపికలు' : 'Recommended Matches'}
                      </strong>
                      <span style={{ fontSize: '11px', color: 'var(--muted-foreground)' }}>
                        {aiResponse?.exact_matches?.length} {language === 'TE' ? 'ఉత్పత్తులు' : 'matches'}
                      </span>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))', gap: '12px' }}>
                      {aiResponse?.exact_matches?.slice(0, 4).map((product) => (
                        <ProductCard
                          key={product.id}
                          product={product}
                          wished={wishlisted.includes(product.id)}
                          isComparing={compareList.some((p) => p.id === product.id)}
                          onWish={() => toggleWishlist(product.id)}
                          onCompare={() => toggleCompare(product)}
                          onAdd={() => addToCart(product)}
                          language={language}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Render Related / Alternative Products */}
                {!isThinking && (aiResponse?.related_products?.length ?? 0) > 0 && (
                  <div style={{ marginTop: '14px', borderTop: '1px solid rgba(20, 93, 79, 0.15)', paddingTop: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                      <strong style={{ fontSize: '12px', color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '5px' }}>
                        <Sparkles size={13} /> {language === 'TE' ? 'మీకు దగ్గరగా ఉన్న ఎంపికలు / ప్రత్యామ్నాయాలు' : 'Closest Alternatives Near Budget'}
                      </strong>
                      <span style={{ fontSize: '11px', color: 'var(--muted-foreground)' }}>
                        {aiResponse?.related_products?.length} {language === 'TE' ? 'ప్రత్యామ్నాయాలు' : 'alternatives'}
                      </span>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))', gap: '12px' }}>
                      {aiResponse?.related_products?.slice(0, 4).map((product) => (
                        <ProductCard
                          key={product.id}
                          product={product}
                          wished={wishlisted.includes(product.id)}
                          isComparing={compareList.some((p) => p.id === product.id)}
                          onWish={() => toggleWishlist(product.id)}
                          onCompare={() => toggleCompare(product)}
                          onAdd={() => addToCart(product)}
                          language={language}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Fallback to products array if exact/related not populated */}
                {!isThinking && !aiResponse?.exact_matches?.length && !aiResponse?.related_products?.length && (aiResponse?.products?.length ?? 0) > 0 && (
                  <div style={{ marginTop: '14px', borderTop: '1px solid rgba(20, 93, 79, 0.15)', paddingTop: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                      <strong style={{ fontSize: '12px', color: 'var(--primary)', display: 'flex', alignItems: 'center', gap: '5px' }}>
                        <Sparkles size={13} /> {language === 'TE' ? 'సిఫార్సు చేయబడిన ఉత్పత్తులు' : 'Recommended Products'}
                      </strong>
                      <span style={{ fontSize: '11px', color: 'var(--muted-foreground)' }}>
                        {aiResponse?.products?.length} {language === 'TE' ? 'ఉత్పత్తులు' : 'matches'}
                      </span>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))', gap: '12px' }}>
                      {aiResponse?.products?.slice(0, 4).map((product) => (
                        <ProductCard
                          key={product.id}
                          product={product}
                          wished={wishlisted.includes(product.id)}
                          isComparing={compareList.some((p) => p.id === product.id)}
                          onWish={() => toggleWishlist(product.id)}
                          onCompare={() => toggleCompare(product)}
                          onAdd={() => addToCart(product)}
                          language={language}
                        />
                      ))}
                    </div>
                  </div>
                )}

                {/* Subscription / Exact-Match Availability Alert Offer */}
                {!isThinking && aiResponse?.subscription_offer?.show && (
                  <div style={{ marginTop: '14px', padding: '12px 14px', borderRadius: '8px', background: 'rgba(255,255,255,0.75)', border: '1px dashed var(--primary)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '7px', marginBottom: '6px', color: 'var(--primary)', fontWeight: 700, fontSize: '12px' }}>
                      <Bell size={14} /> {language === 'TE' ? 'SmartCart లభ్యత అలర్ట్' : 'SmartCart Availability Alert'}
                    </div>
                    <p style={{ fontSize: '12px', color: 'var(--ink-soft)', margin: '0 0 10px 0', lineHeight: 1.45 }}>
                      {aiResponse.subscription_offer.message}
                    </p>
                    {subscribedCategory === aiResponse.subscription_offer.category ? (
                      <div style={{ fontSize: '12px', color: '#047857', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px' }}>
                        <Check size={14} /> {language === 'TE' ? 'అలర్ట్ సెట్ చేయబడింది! మేము మీకు తెలియజేస్తాము.' : 'Alert active! We will notify you.'}
                      </div>
                    ) : (
                      <div style={{ display: 'flex', gap: '8px', maxWidth: '380px' }}>
                        <input 
                          type="email" 
                          placeholder={language === 'TE' ? 'మీ ఇమెయిల్ (ఐచ్ఛికం)' : 'Your email (optional)'}
                          value={subEmail}
                          onChange={(e) => setSubEmail(e.target.value)}
                          style={{ flex: 1, padding: '6px 10px', fontSize: '12px', border: '1px solid var(--border)', borderRadius: '6px', outline: 'none', background: 'white' }}
                        />
                        <button 
                          onClick={() => handleSubscribe(aiResponse.subscription_offer)}
                          disabled={subscribing}
                          style={{ padding: '6px 14px', fontSize: '12px', fontWeight: 700, borderRadius: '6px', background: 'var(--primary)', color: 'white', border: 'none', cursor: 'pointer', whiteSpace: 'nowrap' }}
                        >
                          {subscribing ? '...' : (language === 'TE' ? '🔔 అలర్ట్ సెట్ చేయండి' : '🔔 Notify me when available')}
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {aiResponse?.follow_up_question && (
                  <div className="prompt-examples" style={{ marginTop: '12px' }}>
                    <small style={{ display: 'block', width: '100%', marginBottom: '4px', fontWeight: 600, color: 'var(--primary)' }}>
                      {aiResponse.follow_up_question.question}
                    </small>
                    {aiResponse.follow_up_question.options.map((opt, i) => (
                      <button key={i} onClick={() => submitPrompt(`${prompt} - ${opt}`)}>{opt}</button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Value props */}
      <section className="trust-row">
        <div><Check size={17} /> {language === 'TE' ? 'నిష్పాక్షికమైన సిఫార్సులు' : 'Unbiased recommendations'}</div>
        <div><Check size={17} /> {language === 'TE' ? 'బహుభాషా తెలుగు & ఇంగ్లీష్ AI' : 'Multilingual Telugu & English AI'}</div>
        <div><Check size={17} /> {language === 'TE' ? 'లైవ్ వెక్టర్ డేటాబేస్ సెర్చ్' : 'Live Vector Database search'}</div>
      </section>

      {/* Explore & Recommendations Grid */}
      <section className="section" id="recommendations">
        <div className="section-heading">
          <div>
            <span className="section-kicker">
              {activeSearchQuery
                ? (language === 'TE' ? 'మీ శోధన ఫలితాలు' : 'RECOMMENDED FOR YOUR SEARCH')
                : (selectedCategory !== 'all' ? selectedCategory.toUpperCase() : (language === 'TE' ? 'మీ కోసం ప్రత్యేకంగా' : 'CURATED FOR YOU'))}
            </span>
            <h2>
              {activeSearchQuery
                ? (language === 'TE' ? 'మీ కోసం సిఫార్సులు' : 'Recommended for you')
                : (selectedCategory !== 'all' 
                    ? `${selectedCategory} ${language === 'TE' ? 'కలెక్షన్' : 'Collection'}` 
                    : (language === 'TE' ? 'ఇప్పుడు అత్యంత ప్రాచుర్యం పొందినవి' : 'Popular right now'))}
            </h2>
            <p>
              {activeSearchQuery
                ? (language === 'TE' 
                    ? `"${activeSearchQuery}" కోసం AI ద్వారా ఎంపిక చేయబడిన ${results.length} ఖచ్చితమైన ఉత్పత్తులు.` 
                    : `Showing ${results.length} query-matched products for "${activeSearchQuery}".`)
                : (language === 'TE' ? 'SmartCart ద్వారా ఎంపిక చేయబడిన టాప్ పిక్స్.' : 'Top picks, handpicked by SmartCart.')}
            </p>
          </div>
          {activeSearchQuery ? (
            <button 
              className="text-link" 
              onClick={() => {
                setActiveSearchQuery('')
                setAsked(false)
                if (initialCatalog.length > 0) setCatalogProducts(initialCatalog)
                setSelectedCategory('all')
              }} 
              style={{ background: 'none', border: 'none', cursor: 'pointer' }}
            >
              {language === 'TE' ? 'అన్ని ప్రసిద్ధ ఉత్పత్తులను చూడండి' : 'View all popular products'} <ArrowRight size={15} />
            </button>
          ) : (
            <button onClick={() => setSelectedCategory('all')} className="text-link" style={{ background: 'none', border: 'none', cursor: 'pointer' }}>
              {language === 'TE' ? 'అన్ని కేటగిరీలు చూడండి' : 'View all categories'} <ArrowRight size={15} />
            </button>
          )}
        </div>

        {/* Category Pills Filter */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '24px' }}>
          {['all', 'Electronics', 'Fashion', 'Footwear', 'Accessories', 'Home & Lifestyle', 'Gifts'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              style={{
                padding: '6px 14px',
                borderRadius: '99px',
                fontSize: '12px',
                fontWeight: 600,
                border: '1px solid var(--border)',
                background: selectedCategory.toLowerCase() === cat.toLowerCase() ? 'var(--primary)' : 'white',
                color: selectedCategory.toLowerCase() === cat.toLowerCase() ? 'white' : 'var(--foreground)',
                cursor: 'pointer',
                transition: 'all 0.15s'
              }}
            >
              {cat === 'all' ? (language === 'TE' ? 'అన్ని ఉత్పత్తులు' : 'All Products') : cat}
            </button>
          ))}
        </div>
        
        <div className="product-grid">
          {results.slice(0, 12).map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              wished={wishlisted.includes(product.id)}
              isComparing={compareList.some((p) => p.id === product.id)}
              onWish={() => toggleWishlist(product.id)}
              onCompare={() => toggleCompare(product)}
              onAdd={() => addToCart(product)}
              language={language}
            />
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="how-section" id="how-it-works">
        <div className="section-heading centered">
          <span className="section-kicker">{language === 'TE' ? 'ఇది ఎలా పనిచేస్తుంది' : 'HOW IT WORKS'}</span>
          <h2>{language === 'TE' ? 'షాపింగ్, మరింత స్మార్ట్‌గా.' : 'Shopping, but smarter.'}</h2>
          <p>{language === 'TE' ? 'ప్రశ్న నుండి చెక్‌అవుట్ వరకు కేవలం మూడు సులభమైన దశలు.' : 'From question to checkout in three simple steps.'}</p>
        </div>
        <div className="steps">
          <div className="step">
            <span>01</span>
            <div className="step-icon"><MessageCircle size={21} /></div>
            <h3>{language === 'TE' ? 'మీకు ఏమి కావాలో చెప్పండి' : 'Tell us what you need'}</h3>
            <p>{language === 'TE' ? 'ఇంగ్లీష్ లేదా తెలుగులో మీ స్వంత మాటల్లో అడగండి.' : 'Ask in your own words, in English or Telugu.'}</p>
          </div>
          <div className="step-line" />
          <div className="step">
            <span>02</span>
            <div className="step-icon"><Sparkles size={21} /></div>
            <h3>{language === 'TE' ? 'స్మార్ట్ సిఫార్సులు పొందండి' : 'Get smart recommendations'}</h3>
            <p>{language === 'TE' ? 'మేము మీ అవసరాలకు సరిపోయే ఉత్పత్తులను మ్యాచ్ చేస్తాము.' : 'We match your needs with real catalogue vectors.'}</p>
          </div>
          <div className="step-line" />
          <div className="step">
            <span>03</span>
            <div className="step-icon"><ShoppingCart size={21} /></div>
            <h3>{language === 'TE' ? 'నమ్మకంతో ఎంచుకోండి' : 'Choose with confidence'}</h3>
            <p>{language === 'TE' ? 'పోల్చండి, ఇష్టమైన వాటిని సేవ్ చేయండి, చెక్ అవుట్ చేయండి.' : 'Compare, save favorites, and checkout when ready.'}</p>
          </div>
        </div>
      </section>

      {/* Category cards */}
      <section className="category-section" id="all-products">
        <div className="section-heading">
          <div>
            <span className="section-kicker">{language === 'TE' ? 'కేటగిరీలను అన్వేషించండి' : 'EXPLORE CATEGORIES'}</span>
            <h2>{language === 'TE' ? 'మీకు నచ్చినదాన్ని కనుగొనండి.' : 'Find your next favorite.'}</h2>
          </div>
        </div>
        <div className="category-grid">
          <Link href="#recommendations" onClick={() => filterByCategory('Audio')} className="category-card category-audio">
            <span>{language === 'TE' ? 'ఆడియో' : 'Audio'}</span>
            <small>{language === 'TE' ? 'ఇయర్‌బడ్స్, హెడ్‌ఫోన్స్ & మరిన్ని' : 'Earbuds, headphones & more'} <ArrowRight size={14} /></small>
          </Link>
          <Link href="#recommendations" onClick={() => filterByCategory('Laptops')} className="category-card category-work">
            <span>{language === 'TE' ? 'ఆఫీస్ & వర్క్ ఎస్సెన్షియల్స్' : 'Work essentials'}</span>
            <small>{language === 'TE' ? 'మానిటర్లు, ల్యాప్‌టాప్‌లు & ఉపకరణాలు' : 'Monitors, laptops & accessories'} <ArrowRight size={14} /></small>
          </Link>
          <Link href="#recommendations" onClick={() => filterByCategory('Home & Lifestyle')} className="category-card category-home">
            <span>{language === 'TE' ? 'హోమ్ & లివింగ్' : 'Home & living'}</span>
            <small>{language === 'TE' ? 'మీ ఇంటిని మరింత అందంగా మార్చండి' : 'Make your space better'} <ArrowRight size={14} /></small>
          </Link>
        </div>
      </section>

      {/* Newsletter */}
      <section className="newsletter">
        <div>
          <span className="section-kicker">{language === 'TE' ? 'అప్‌డేట్స్ పొందండి' : 'STAY IN THE LOOP'}</span>
          <h2>{language === 'TE' ? 'స్మార్ట్ ఆఫర్లు, నేరుగా మీ ఇన్‌బాక్స్‌కి.' : 'Smarter finds, straight to your inbox.'}</h2>
          <p>{language === 'TE' ? 'వారపు ఉత్తమ పిక్స్ మరియు ధరల తగ్గింపులు. ఎటువంటి స్పామ్ ఉండదు.' : 'Weekly picks, price drops, and shopping tips. No spam, ever.'}</p>
        </div>
        <form onSubmit={(e) => { e.preventDefault(); setToast('Subscribed successfully!'); setTimeout(() => setToast(''), 2500) }}>
          <input type="email" placeholder="Your email address" aria-label="Email address" required />
          <button type="submit">{language === 'TE' ? 'సబ్‌స్క్రైబ్' : 'Subscribe'}</button>
        </form>
      </section>

      {/* Footer */}
      <footer>
        <Link href="/" aria-label="SmartCart Home" onClick={() => setSelectedCategory('all')}>
          <Logo size="sm" />
        </Link>
        <span>{language === 'TE' ? 'మెరుగైన షాపింగ్ నిర్ణయాల కోసం రూపొందించబడింది.' : 'Made for better decisions.'}</span>
        <div>
          <button className="language" onClick={() => setCompareOpen(true)}>{language === 'TE' ? 'పోల్చండి' : 'Compare'} ({compareList.length})</button>
          <button className="language" onClick={openOrdersModal}>{language === 'TE' ? 'ఆర్డర్లు' : 'Orders'}</button>
          <button className="language" onClick={() => setCartOpen(true)}>{language === 'TE' ? 'కార్ట్' : 'Cart'} ({totalCartCount})</button>
        </div>
      </footer>

      {/* ========================================================================= */}
      {/* 1. CART SLIDE-OVER DRAWER */}
      {/* ========================================================================= */}
      {cartOpen && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 50, display: 'flex', justifyContent: 'flex-end', background: 'rgba(0,0,0,0.45)', backdropFilter: 'blur(4px)' }}>
          <div style={{ width: '100%', maxWidth: '440px', background: 'white', height: '100%', display: 'flex', flexDirection: 'column', boxShadow: '-10px 0 30px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px 24px', borderBottom: '1px solid var(--border)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <ShoppingCart size={20} color="var(--primary)" />
                <strong>{language === 'TE' ? 'మీ షాపింగ్ కార్ట్' : 'Your Shopping Cart'} ({cartData?.item_count || 0})</strong>
              </div>
              <button onClick={() => { setCartOpen(false); setCheckoutStep(false) }} style={{ border: 0, background: 'transparent', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', padding: '20px 24px' }}>
              {!checkoutStep ? (
                <>
                  {!cartData || cartData.items.length === 0 ? (
                    <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--muted-foreground)' }}>
                      <ShoppingCart size={40} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
                      <p>{language === 'TE' ? 'మీ కార్ట్ ఖాళీగా ఉంది.' : 'Your cart is empty.'}</p>
                      <button onClick={() => setCartOpen(false)} className="add-button" style={{ marginTop: '12px', justifyContent: 'center' }}>
                        {language === 'TE' ? 'ఉత్పత్తులను చూడండి' : 'Browse products'}
                      </button>
                    </div>
                  ) : (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                      {cartData.items.map((item) => (
                        <div key={item.product_id} style={{ display: 'flex', gap: '12px', paddingBottom: '16px', borderBottom: '1px solid var(--border)' }}>
                          <img src={item.product?.image} alt={item.product?.name} style={{ width: '70px', height: '70px', objectFit: 'cover', borderRadius: '8px' }} />
                          <div style={{ flex: 1 }}>
                            <h4 style={{ margin: '0 0 4px', fontSize: '13px', fontWeight: 600 }}>{item.product?.name}</h4>
                            <div style={{ color: 'var(--primary)', fontWeight: 700, fontSize: '14px', marginBottom: '8px' }}>
                              {money(item.unit_price)}
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', border: '1px solid var(--border)', borderRadius: '6px', padding: '2px 6px' }}>
                                <button onClick={() => updateCartQty(item.product_id, item.quantity - 1)} style={{ border: 0, background: 'transparent', cursor: 'pointer' }}>
                                  <Minus size={12} />
                                </button>
                                <span style={{ fontSize: '12px', fontWeight: 700 }}>{item.quantity}</span>
                                <button onClick={() => updateCartQty(item.product_id, item.quantity + 1)} style={{ border: 0, background: 'transparent', cursor: 'pointer' }}>
                                  <Plus size={12} />
                                </button>
                              </div>
                              <button onClick={() => removeCartItem(item.product_id)} style={{ border: 0, background: 'transparent', color: '#b25756', cursor: 'pointer' }}>
                                <Trash2 size={15} />
                              </button>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                /* Demo Checkout Form */
                <div>
                  <h3 style={{ margin: '0 0 16px', fontSize: '16px' }}>Shipping Address (Demo)</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                    <div>
                      <label style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted-foreground)' }}>Full Name</label>
                      <input
                        type="text"
                        value={shippingAddress.full_name}
                        onChange={(e) => setShippingAddress({ ...shippingAddress, full_name: e.target.value })}
                        style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--border)', borderRadius: '6px', marginTop: '4px' }}
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted-foreground)' }}>Phone Number</label>
                      <input
                        type="text"
                        value={shippingAddress.phone}
                        onChange={(e) => setShippingAddress({ ...shippingAddress, phone: e.target.value })}
                        style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--border)', borderRadius: '6px', marginTop: '4px' }}
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted-foreground)' }}>Delivery Address</label>
                      <input
                        type="text"
                        value={shippingAddress.address_line}
                        onChange={(e) => setShippingAddress({ ...shippingAddress, address_line: e.target.value })}
                        style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--border)', borderRadius: '6px', marginTop: '4px' }}
                      />
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                      <div>
                        <label style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted-foreground)' }}>City</label>
                        <input
                          type="text"
                          value={shippingAddress.city}
                          onChange={(e) => setShippingAddress({ ...shippingAddress, city: e.target.value })}
                          style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--border)', borderRadius: '6px', marginTop: '4px' }}
                        />
                      </div>
                      <div>
                        <label style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted-foreground)' }}>PIN Code</label>
                        <input
                          type="text"
                          value={shippingAddress.pincode}
                          onChange={(e) => setShippingAddress({ ...shippingAddress, pincode: e.target.value })}
                          style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--border)', borderRadius: '6px', marginTop: '4px' }}
                        />
                      </div>
                    </div>

                    <div style={{ marginTop: '10px' }}>
                      <label style={{ fontSize: '11px', fontWeight: 700, color: 'var(--muted-foreground)' }}>Payment Method (Demo Mode)</label>
                      <div style={{ display: 'flex', gap: '8px', marginTop: '6px' }}>
                        {['UPI', 'Card', 'COD'].map((pm) => (
                          <button
                            key={pm}
                            onClick={() => setPaymentMethod(pm)}
                            style={{
                              flex: 1,
                              padding: '8px',
                              borderRadius: '6px',
                              border: `1px solid ${paymentMethod === pm ? 'var(--primary)' : 'var(--border)'}`,
                              background: paymentMethod === pm ? 'var(--accent)' : 'white',
                              fontWeight: paymentMethod === pm ? 700 : 400,
                              color: paymentMethod === pm ? 'var(--primary)' : 'var(--foreground)',
                              cursor: 'pointer'
                            }}
                          >
                            {pm}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Cart Summary Footer */}
            {cartData && cartData.items.length > 0 && (
              <div style={{ padding: '20px 24px', borderTop: '1px solid var(--border)', background: '#fafbfc' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '6px' }}>
                  <span>{language === 'TE' ? 'సబ్‌టోటల్' : 'Subtotal'}</span>
                  <span>{money(cartData.subtotal)}</span>
                </div>
                {cartData.discount > 0 && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', color: '#16a34a', marginBottom: '6px' }}>
                    <span>{language === 'TE' ? 'ఆదా' : 'Savings'}</span>
                    <span>-{money(cartData.discount)}</span>
                  </div>
                )}
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', marginBottom: '12px' }}>
                  <span>{language === 'TE' ? 'డెలివరీ' : 'Delivery'}</span>
                  <span>{cartData.delivery === 0 ? 'FREE' : money(cartData.delivery)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 700, fontSize: '16px', marginBottom: '16px' }}>
                  <span>{language === 'TE' ? 'మొత్తం ధర' : 'Total Amount'}</span>
                  <span style={{ color: 'var(--primary)' }}>{money(cartData.total)}</span>
                </div>

                {!checkoutStep ? (
                  <button
                    onClick={() => setCheckoutStep(true)}
                    style={{ width: '100%', padding: '12px', borderRadius: '8px', color: 'white', background: 'var(--primary)', border: 0, fontWeight: 700, cursor: 'pointer' }}
                  >
                    {language === 'TE' ? 'చెక్‌అవుట్‌కి వెళ్లండి' : 'Proceed to Checkout'}
                  </button>
                ) : (
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      onClick={() => setCheckoutStep(false)}
                      style={{ padding: '12px', borderRadius: '8px', border: '1px solid var(--border)', background: 'white', cursor: 'pointer' }}
                    >
                      {language === 'TE' ? 'వెనుకకు' : 'Back'}
                    </button>
                    <button
                      onClick={handlePlaceOrder}
                      style={{ flex: 1, padding: '12px', borderRadius: '8px', color: 'white', background: 'var(--primary)', border: 0, fontWeight: 700, cursor: 'pointer' }}
                    >
                      {language === 'TE' ? 'ఆర్డర్ ప్లేస్ చేయండి' : 'Place Demo Order'} ({money(cartData.total)})
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 2. COMPARE MODAL */}
      {/* ========================================================================= */}
      {compareOpen && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 50, display: 'grid', placeItems: 'center', background: 'rgba(0,0,0,0.5)', padding: '20px' }}>
          <div style={{ width: '100%', maxWidth: '850px', background: 'white', borderRadius: '16px', maxHeight: '90vh', display: 'flex', flexDirection: 'column', overflow: 'hidden', boxShadow: '0 20px 50px rgba(0,0,0,0.2)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '18px 24px', borderBottom: '1px solid var(--border)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Scale size={20} color="var(--primary)" />
                <strong>{language === 'TE' ? 'ఉత్పత్తుల పోలిక' : 'Product Comparison'} ({compareList.length}/4)</strong>
              </div>
              <button onClick={() => setCompareOpen(false)} style={{ border: 0, background: 'transparent', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', padding: '24px' }}>
              {compareList.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--muted-foreground)' }}>
                  <Scale size={40} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
                  <p>{language === 'TE' ? 'పోల్చడానికి ఉత్పత్తులు ఇంకా ఎంచుకోలేదు.' : 'No products selected for comparison yet.'}</p>
                  <small>{language === 'TE' ? 'ఉత్పత్తి కార్డ్ లో "Compare" నొక్కి ఇక్కడ చేర్చండి.' : 'Click "Compare" on any product card in the catalogue to add products here.'}</small>
                </div>
              ) : (
                <>
                  <div style={{ display: 'grid', gridTemplateColumns: `repeat(${compareList.length}, 1fr)`, gap: '16px', marginBottom: '24px' }}>
                    {compareList.map((prod) => (
                      <div key={prod.id} style={{ border: '1px solid var(--border)', borderRadius: '10px', padding: '12px', display: 'flex', flexDirection: 'column' }}>
                        <div style={{ position: 'relative', height: '120px', marginBottom: '8px' }}>
                          <img src={prod.image} alt={prod.name} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '6px' }} />
                          <button
                            onClick={() => toggleCompare(prod)}
                            style={{ position: 'absolute', top: '4px', right: '4px', background: 'rgba(0,0,0,0.6)', color: 'white', border: 0, borderRadius: '50%', width: '22px', height: '22px', display: 'grid', placeItems: 'center', cursor: 'pointer' }}
                          >
                            <X size={12} />
                          </button>
                        </div>
                        <span style={{ fontSize: '10px', color: 'var(--muted-foreground)', textTransform: 'uppercase' }}>{prod.category}</span>
                        <h4 style={{ margin: '2px 0 6px', fontSize: '13px' }}>{prod.name}</h4>
                        <div style={{ color: 'var(--primary)', fontWeight: 700, fontSize: '15px' }}>{money(prod.price)}</div>
                        <div style={{ fontSize: '11px', color: '#c18b3a', display: 'flex', alignItems: 'center', gap: '3px', margin: '4px 0 8px' }}>
                          <Star size={12} fill="currentColor" /> {prod.rating}
                        </div>
                        
                        <div style={{ borderTop: '1px solid var(--border)', paddingTop: '8px', marginTop: 'auto' }}>
                          <ul style={{ paddingLeft: '14px', margin: 0, fontSize: '11px', color: 'var(--ink-soft)' }}>
                            {prod.specs.slice(0, 3).map((spec, i) => (
                              <li key={i}>{spec}</li>
                            ))}
                          </ul>
                        </div>
                        
                        <button onClick={() => addToCart(prod)} className="add-button" style={{ marginTop: '10px' }}>
                          {language === 'TE' ? 'కార్ట్‌కి జోడించు' : 'Add to cart'} <ArrowRight size={13} />
                        </button>
                      </div>
                    ))}
                  </div>

                  {compareList.length >= 2 && (
                    <div style={{ background: 'var(--accent)', borderRadius: '12px', padding: '16px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--primary)', fontWeight: 700, fontSize: '13px' }}>
                          <Sparkles size={16} /> {language === 'TE' ? 'AI పోలిక విశ్లేషణ' : 'AI Comparison Summary'}
                        </div>
                        <button
                          onClick={runAiCompare}
                          disabled={isComparing}
                          style={{ padding: '5px 12px', borderRadius: '6px', background: 'var(--primary)', color: 'white', border: 0, fontSize: '11px', fontWeight: 600, cursor: 'pointer' }}
                        >
                          {isComparing ? (language === 'TE' ? 'విశ్లేషిస్తోంది...' : 'Analyzing...') : (language === 'TE' ? 'విశ్లేషణ రూపొందించండి' : 'Generate Insights')}
                        </button>
                      </div>
                      <p style={{ margin: 0, fontSize: '12px', color: 'var(--ink-soft)', lineHeight: 1.6 }}>
                        {compareExplanation || `Click 'Generate Insights' to receive an objective breakdown of value, specifications, and advantages between ${compareList.map((p) => p.name).join(' and ')}.`}
                      </p>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* 3. ORDERS MODAL */}
      {/* ========================================================================= */}
      {ordersOpen && (
        <div style={{ position: 'fixed', inset: 0, zIndex: 50, display: 'grid', placeItems: 'center', background: 'rgba(0,0,0,0.5)', padding: '20px' }}>
          <div style={{ width: '100%', maxWidth: '650px', background: 'white', borderRadius: '16px', maxHeight: '85vh', display: 'flex', flexDirection: 'column', overflow: 'hidden', boxShadow: '0 20px 50px rgba(0,0,0,0.2)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '18px 24px', borderBottom: '1px solid var(--border)' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Package size={20} color="var(--primary)" />
                <strong>{language === 'TE' ? 'మీ ఆర్డర్ల హిస్టరీ' : 'Your Order History'}</strong>
              </div>
              <button onClick={() => setOrdersOpen(false)} style={{ border: 0, background: 'transparent', cursor: 'pointer' }}>
                <X size={20} />
              </button>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', padding: '24px' }}>
              {ordersList.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--muted-foreground)' }}>
                  <Package size={40} style={{ margin: '0 auto 12px', opacity: 0.3 }} />
                  <p>{language === 'TE' ? 'ఈ సెషన్‌లో ఇంకా ఎలాంటి ఆర్డర్లు లేవు.' : 'No orders placed in this session yet.'}</p>
                  <small>{language === 'TE' ? 'ఉత్పత్తులను కార్ట్‌కి జోడించి చెక్‌అవుట్ చేయండి.' : 'Add products to your cart and proceed to checkout to place demo orders.'}</small>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                  {ordersList.map((order) => (
                    <div key={order.id} style={{ border: '1px solid var(--border)', borderRadius: '12px', padding: '16px', background: '#fafbfc' }}>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px', borderBottom: '1px solid var(--border)', paddingBottom: '10px' }}>
                        <div>
                          <strong style={{ fontSize: '13px' }}>{order.order_id}</strong>
                          <span style={{ display: 'block', fontSize: '11px', color: 'var(--muted-foreground)' }}>
                            {new Date(order.created_at).toLocaleString()}
                          </span>
                        </div>
                        <span style={{ padding: '4px 10px', borderRadius: '99px', fontSize: '10px', fontWeight: 800, textTransform: 'uppercase', background: '#e0f2fe', color: '#0369a1' }}>
                          {order.status}
                        </span>
                      </div>

                      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: '12px' }}>
                        {order.items.map((item, idx) => (
                          <div key={idx} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                            <span>{item.product?.name || item.product_id} × {item.quantity}</span>
                            <span style={{ fontWeight: 600 }}>{money(item.total_price)}</span>
                          </div>
                        ))}
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border)', paddingTop: '10px' }}>
                        <div style={{ fontSize: '11px', color: 'var(--muted-foreground)' }}>
                          {language === 'TE' ? 'చెల్లింపు విధానం:' : 'Paid via'} <strong>{order.payment_method}</strong> (Demo)
                        </div>
                        <div style={{ fontSize: '14px', fontWeight: 700, color: 'var(--primary)' }}>
                          {language === 'TE' ? 'మొత్తం:' : 'Total:'} {money(order.total)}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </main>
  )
}

function ProductCard({
  product,
  wished,
  isComparing,
  onWish,
  onCompare,
  onAdd,
  language
}: {
  product: Product
  wished: boolean
  isComparing: boolean
  onWish: () => void
  onCompare: () => void
  onAdd: () => void
  language?: 'EN' | 'TE'
}) {
  return (
    <article className="product-card">
      <div className="product-image-wrap">
        <img src={product.image} alt={product.name} className="product-image" loading="lazy" />
        <button
          className={`wish-button ${wished ? 'wished' : ''}`}
          onClick={onWish}
          aria-label={`Save ${product.name}`}
        >
          <Heart size={18} fill={wished ? 'currentColor' : 'none'} />
        </button>
        {product.budget_status === 'above_budget' && product.budget_difference ? (
          <span className="product-badge" style={{ background: '#fef3c7', color: '#92400e', border: '1px solid #fde68a', fontWeight: 700 }}>
            {language === 'TE' ? `+₹${product.budget_difference.toLocaleString('en-IN')} బడ్జెట్ కంటే ఎక్కువ` : `+₹${product.budget_difference.toLocaleString('en-IN')} above budget`}
          </span>
        ) : product.badge ? (
          <span className="product-badge">{product.badge}</span>
        ) : null}
      </div>
      <div className="product-info">
        <span className="product-category">{product.category}</span>
        <h3>{product.name}</h3>
        <div className="rating">
          <Star size={14} fill="currentColor" /> {product.rating} <span>({product.reviews.toLocaleString()})</span>
        </div>
        <div className="price-row">
          <strong>{money(product.price)}</strong>
          {product.oldPrice && <del>{money(product.oldPrice)}</del>}
        </div>

        {product.why_recommended ? (
          <div style={{ fontSize: '11px', color: 'var(--primary)', background: 'var(--accent)', padding: '5px 8px', borderRadius: '6px', marginBottom: '8px', lineHeight: 1.35, fontWeight: 500 }}>
            <span style={{ fontWeight: 700 }}>{language === 'TE' ? 'సిఫార్సు:' : 'Why:'}</span> {product.why_recommended}
          </div>
        ) : (
          product.specs && product.specs.length > 0 && (
            <div style={{ fontSize: '11px', color: 'var(--muted-foreground)', marginBottom: '8px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {product.specs.slice(0, 2).join(' • ')}
            </div>
          )
        )}
        
        <div style={{ display: 'flex', gap: '6px' }}>
          <button
            onClick={onCompare}
            style={{
              padding: '10px',
              borderRadius: '7px',
              border: `1px solid ${isComparing ? 'var(--primary)' : '#cfe0db'}`,
              background: isComparing ? 'var(--accent)' : 'white',
              color: isComparing ? 'var(--primary)' : 'var(--foreground)',
              fontSize: '11px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '4px'
            }}
            title="Compare product"
          >
            <Scale size={13} />
            {isComparing ? (language === 'TE' ? 'చేర్చబడింది' : 'Added') : (language === 'TE' ? 'పోల్చండి' : 'Compare')}
          </button>
          <button className="add-button" onClick={onAdd} style={{ flex: 1 }}>
            {language === 'TE' ? 'కార్ట్‌కి జోడించు' : 'Add to cart'} <ArrowRight size={15} />
          </button>
        </div>
      </div>
    </article>
  )
}
