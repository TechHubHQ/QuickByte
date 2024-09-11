import React from "react";
import { Mail } from "lucide-react";
import { FacebookIcon, TwitterIcon, InstagramIcon, GithubIcon } from "./icons"

const Footer: React.FC = () => {
  return (
    <footer
      className="bg-base-200 text-base-content rounded-t-[10px] shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.4)] hover:shadow-[0_-4px_8px_-1px_rgba(0,0,0,0.5)] transition-shadow duration-300 ease-in-out"
    >
      <div className="container mx-auto py-10 px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Company Info */}
          <div className="flex flex-col items-center md:items-start">
            <h2
              className="text-2xl font-bold mb-4"
              style={{ fontFamily: "'Pacifico', cursive" }}
            >
              QuickByte
            </h2>
            <p className="text-sm text-center md:text-left">
              Delivering delicious meals at lightning speed.
            </p>
          </div>

          {/* Quick Links */}
          <div className="flex flex-col items-center md:items-start">
            <h3 className="text-lg font-semibold mb-4">QuickVerse</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  QuickMart
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-primary transition-colors">
                  QuickKart
                </a>
              </li>
            </ul>
          </div>

          {/* Social Media */}
          <div className="flex flex-col items-center md:items-start">
            <h3 className="text-lg font-semibold mb-4">Connect With Us</h3>
            <div className="flex space-x-4">
              <a href="#" className="hover:opacity-80 transition-opacity">
                <FacebookIcon />
              </a>
              <a href="#" className="hover:opacity-80 transition-opacity">
                <TwitterIcon />
              </a>
              <a href="#" className="hover:opacity-80 transition-opacity">
                <InstagramIcon />
              </a>
              <a href="#" className="hover:opacity-80 transition-opacity">
                <GithubIcon />
              </a>
              <a href="#" className="hover:text-primary transition-colors">
                <Mail size={20} className="text-red-500" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-8 pt-8 border-t border-base-300 text-sm text-center">
          <p>
            &copy; {new Date().getFullYear()} QuickByte. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
