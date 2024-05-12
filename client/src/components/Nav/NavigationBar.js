import './NavigationBar.css'
import { useState, useEffect } from 'react'
import { RxHamburgerMenu as OpenMenu } from "react-icons/rx"
import { CgClose as HideMenu} from 'react-icons/cg' 
import { Link } from 'react-router-dom';


const NavigationBar = () => {
  const [menuOpen, setMenuOpen] = useState(false)
  const [width, setWidth] = useState(window.innerWidth)

  useEffect(() => {
    const handleResize = () => {
      setWidth(window.innerWidth)
      window.innerWidth > 1200 && setMenuOpen(false)
    }
    window.addEventListener('resize', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  return (
    <>
      <nav className="navBar">
        <div className="leftSection">
          
            <div className='companyLogo'>
              {/* <img src=''/> */}
              <h1>Finacle</h1>
            </div>
        
            <div className="navBtns">
          
            <a href="#"><Link to="/">Home</Link></a>            
        {/* <li><a href="#"><Link to="/Irc">IRC 2024</Link></a></li>   */}


              <div className="navDropdown">
              <a href="#"><Link to="/home">Scheme</Link></a> 
                {/* <div className="aboutDropdownMenu">
                </div> */}
              </div>
              <div className="navDropdown">
              <a href="#"><Link to="/detail">Proposal</Link></a> 
                {/* <div className="serviceDropdownMenu">
                 
                </div> */}
              </div>
              
              
              {/* <button>Blog</button>
              <button>News</button> */}
            </div>
        </div>
        <div className='rightSection'>
          <div className="accountSection">
            <button>Login</button>
            <button>Sign Up</button>
          </div>
          <div className="menuSection">
            {
              !menuOpen ? 
                <OpenMenu className='menuBtn' onClick={() => setMenuOpen(true)}/> : 
                <HideMenu className='hideBtn' onClick={() => setMenuOpen(false)}/>
            }
          </div>
        </div>
        
      </nav>
    </>
  )
}

export default NavigationBar