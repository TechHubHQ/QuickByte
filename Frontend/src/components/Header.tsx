import React from "react";
import logo from "../assets/logo.png";
import { LogIn, UserPlus } from "lucide-react";

const Navbar: React.FC = () => {
  return (
    <div className="navbar bg-base-100 shadow-[0_4px_6px_-1px_rgba(0,0,0,0.3)] hover:shadow-[0_4px_8px_-1px_rgba(0,0,0,0.4)] transition-shadow duration-300 ease-in-out rounded-b-[10px] h-24">
      <div className="navbar-start pl-6">
        <a 
          className="normal-case text-xl flex items-center"
          style={{ fontFamily: "'Pacifico', cursive", fontSize: "1.5rem" }}
        >
          <img src={logo} alt="QuickByte Logo" className="h-20 w-20 mr-1" />
          QuickByte
        </a>
      </div>
      <div className="navbar-end pr-4">
        {/* Desktop menu */}
        <ul className="menu menu-horizontal px-1 hidden lg:flex">
          <li className="mr-4">
            <button
              className="btn btn-sm btn-error flex items-center"
              style={{ fontFamily: "'Roboto', sans-serif" }}
            >
              <LogIn className="w-5 h-5 mr-1" />
              Login
            </button>
          </li>
          <li>
            <button
              className="btn btn-sm btn-success flex items-center"
              style={{ fontFamily: "'Roboto', sans-serif" }}
            >
              <UserPlus className="w-5 h-5 mr-1" />
              Sign Up
            </button>
          </li>
        </ul>
        {/* Mobile menu */}
        <div className="dropdown dropdown-end lg:hidden">
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h16M4 18h7"
              />
            </svg>
          </div>
          <ul
            tabIndex={0}
            className="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow"
          >
            <li className="mb-2">
              <button
                className="btn btn-sm btn-error flex items-center w-full"
                style={{ fontFamily: "'Roboto', sans-serif" }}
              >
                <LogIn className="w-5 h-5 mr-2" />
                Login
              </button>
            </li>
            <li>
              <button
                className="btn btn-sm btn-success flex items-center w-full"
                style={{ fontFamily: "'Roboto', sans-serif" }}
              >
                <UserPlus className="w-5 h-5 mr-2" />
                Sign Up
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
