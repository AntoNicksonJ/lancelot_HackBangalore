import { useEffect, useRef } from 'react'
import './AboutSection.css'
import pi1 from "../assets/Bank2.png"


const AboutSection = () => {
  const aboutImageRef = useRef()

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting)
          entry.target.classList.add("fadeIn")
      })
    }, {
      threshold: 0.5
    })
    observer.observe(aboutImageRef.current)
  }, [])

  return (
    <section className='aboutSection'>
      <div className="aboutLeft">
        <img 
          src={pi1} 
          className='aboutImage'
          ref={aboutImageRef} 
          width={750} height={450}/>
      </div>
      <div className="aboutRight">
        <div className="header">
        <p>AI-powered loan suggestion.</p>
        </div>
        <div className="body">
        <p>Experience a revolutionary lending solution powered by our AI platform. Our advanced agent evaluates loan requests for banks, ensuring growth and mitigating risks. Simultaneously, it empowers customers by highlighting government schemes for financial benefits. Streamlined processes and informed decisions await, driven by cutting-edge technology.</p></div>
        <div className="button">
          <button>Get Start</button>
        </div>
      </div>
    </section>
  )
}

export default AboutSection