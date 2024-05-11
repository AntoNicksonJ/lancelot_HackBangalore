import { useEffect, useRef } from 'react'
import './Welcome.css'
import pi2 from "../assets/Bank1.png"

const WelcomeSection = () => {
  const welcomeImageRef = useRef()

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting)
          entry.target.classList.add("fadeIn")
      })
    }, {
      threshold: 0.5
    })
    observer.observe(welcomeImageRef.current)
  }, [])

  return (    
    <section className="welcomeSection">
      <div className="welcomeText">
        <div className="motto">
        <p>Effortless loans</p>
        </div>
        <div className="mottoSubtitle">
        <p>Empowering borrowers and lenders alike, our platform streamlines loan applications, matches users with tailored loan options, and illuminates government and private loan schemes for financial success.</p></div>
        <div className="welcomeButtons">
          <button>Get Start</button>
        </div>
      </div>
      <div className="imageSection">
        <img 
          src={pi2} 
          className='welcomeImage'
          ref={welcomeImageRef} 
          width={576*1.1} height={360*1.1}/>
      </div>
    </section>
  )
}

export default WelcomeSection