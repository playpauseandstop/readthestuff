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
      <footer className="container footer text-muted">
        <hr />
        <div className="row">
          <div className="col-xs-6">
            <ul className="list-inline">
              <li>&copy; 2015 <Link to="landing">Read the Stuff</Link></li>
              <li><Link to="terms">Terms</Link></li>
              <li><Link to="privacy">Privacy</Link></li>
              <li><Link to="contact">Contact</Link></li>
            </ul>
          </div>
          <div className="col-xs-6 text-right">
            <ul className="list-inline">
              <li><a href="#">Status</a></li>
              <li><a href="#">Blog</a></li>
              <li><Link to="about">About</Link></li>
            </ul>
          </div>
        </div>
      </footer>
    );
  }
}

Footer.displayName = "Footer";


export default Footer;
