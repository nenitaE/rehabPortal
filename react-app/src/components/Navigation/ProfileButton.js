import React, { useState, useEffect, useRef } from "react";
import { useDispatch } from "react-redux";
import { logout } from "../../store/session";
import { NavLink } from "react-router-dom/cjs/react-router-dom";
import OpenModalButton from "../OpenModalButton";
import LoginFormModal from "../LoginFormModal";
import SignupFormModal from "../SignupFormModal";

function ProfileButton({ user }) {
  const dispatch = useDispatch();
  const [showMenu, setShowMenu] = useState(false);
  const ulRef = useRef();

  const openMenu = () => {
    if (showMenu) return;
    setShowMenu(true);
  };

  useEffect(() => {
    if (!showMenu) return;

    const closeMenu = (e) => {
      if (!ulRef.current.contains(e.target)) {
        setShowMenu(false);
      }
    };

    document.addEventListener("click", closeMenu);

    return () => document.removeEventListener("click", closeMenu);
  }, [showMenu]);

  const handleLogout = (e) => {
    e.preventDefault();
    dispatch(logout());
  };

  const ulClassName = "profile-dropdown" + (showMenu ? "" : " hidden");
  const closeMenu = () => setShowMenu(false);

  return (
    <>
      <div className="profileButtonContainer">
        <button id="navProfileBTTN" onClick={openMenu}>
        <i className="fa-solid fa-bars" style={{color: "#1e0048",}} />
        </button>
        <ul className={ulClassName} ref={ulRef}>
          {user ? (
            <>
              <img src={user.profileImage} alt="profileImage" width="70" height="70" className="menu-profile-image"/>
              <li className="welcome-profile">Welcome {user.isClinician && <>Dr. </>}{user.firstName}</li>
              <li>{user.email}</li>
              <li className="link-profileBttn">
                <NavLink className='text-link-profileBttn' to="/patientLists/current">Patient List</NavLink>
              </li>
              <li>
                <button onClick={handleLogout}>Log Out</button>
              </li>
            </>
          ) : (
            <>
              <OpenModalButton
                buttonText="Log In"
                onItemClick={closeMenu}
                modalComponent={<LoginFormModal />}
              />

              <OpenModalButton
                buttonText="Sign Up"
                onItemClick={closeMenu}
                modalComponent={<SignupFormModal />}
              />
            </>
          )}
        </ul>
      </div>
    </>
  );
}

export default ProfileButton;
