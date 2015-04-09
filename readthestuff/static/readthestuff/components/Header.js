/**
 * Header
 * ======
 *
 * Header component to show for logged in users.
 *
 */

"use strict";

import React from "react";
import Link from "react-router";


class Header extends React.Component {
  render() {
    return (
      <header className="header">
        <h1>Read the Stuff</h1>
        <ul>
          <li>Hello, {this.props.user.displayName}</li>
          <li><Link to="logout">Sign Out</Link></li>
        </ul>
      </header>
    );
  }
}

Header.displayName = "Header";
Header.propTypes = {
  user: React.PropTypes.shape({
    displayName: React.PropTypes.string.isRequired
  })
};


export default Header;
