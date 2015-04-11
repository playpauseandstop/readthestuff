/**
 * Login Page
 * ==========
 *
 * Links to login for Read the Stuff project via external providers.
 *
 */

"use strict";

import React from "react";
import { Link } from "react-router";


class LoginPage extends React.Component {
  render() {
    return (
      <div className="container container-main login-buttons">
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4 text-center text-muted">
            Login With
          </div>
        </div>
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4">
            <a className="btn btn-block btn-primary" href="#google">Google</a>
          </div>
        </div>
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4">
            <a className="btn btn-block btn-primary" href="#dropbox">Dropbox</a>
          </div>
        </div>
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4">
            <a className="btn btn-block btn-primary" href="#facebook">Facebook</a>
          </div>
        </div>
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4">
            <a className="btn btn-block btn-primary" href="#twitter">Twitter</a>
          </div>
        </div>
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4 text-center text-muted">
            or
          </div>
        </div>
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-sm-offset-3 col-md-4 col-md-offset-4">
            <Link className="btn btn-block btn-danger" to="landing">Cancel</Link>
          </div>
        </div>
      </div>
    );
  }
}

LoginPage.displayName = "Login Page";


export default LoginPage;
