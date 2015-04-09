/**
 * Footer
 * ======
 *
 * Unify footer element for show on all pages.
 *
 */

"use strict";

import React from "react";
import { Link } from "react-router";


class Footer extends React.Component {
  render() {
    return (
      <footer className="footer">
        <div className="container text-muted">
          <span className="whitespace-after">
            <a href="http://igordavydenko.com/">Igor Davydenko</a>
            project.
          </span>
          <br className="visible-xs-block" />
          <ul>
            <li><Link to="about">About</Link></li>
            <li><Link to="terms">Terms</Link></li>
            <li><Link to="privacy">Privacy</Link></li>
            <li><Link to="contact">Contact</Link></li>
          </ul>
          <span>Made in Ukraine. 2013-2015</span>
        </div>
      </footer>
    );
  }
}

Footer.displayName = "Footer";


export default Footer;
