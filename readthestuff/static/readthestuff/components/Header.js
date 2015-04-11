/**
 * Header
 * ======
 *
 * Header component to show for logged in users.
 *
 */

"use strict";

import _ from "underscore";
import React from "react";
import { Link } from "react-router";


class Header extends React.Component {
  render() {
    if (_.isEmpty(this.props.user)) {
      return (
        <header className="container header">
          <div className="row">
            <div className="col-xs-12 col-sm-9 col-lg-10">
              <h1>Read the Stuff</h1>
            </div>
            <div className="col-xs-12 col-sm-3 col-lg-2">
              <Link className="btn btn-block btn-success" to="login">
                Login
              </Link>
            </div>
          </div>
          <hr />
        </header>
      );
    }
    return null;
  }
}

Header.displayName = "Header";
Header.propTypes = {
  user: React.PropTypes.object
};


export default Header;
