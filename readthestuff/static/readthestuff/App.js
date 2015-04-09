/**
 * Read the Stuff
 * ==============
 *
 * Main application for Read the Stuff frontend.
 *
 */

/* global self */

"use strict";

import "whatwg-fetch";
import _ from "underscore";
import React, { PropTypes } from "react";
import Router, { DefaultRoute, Route, RouteHandler } from "react-router";

import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import DashboardPage from "./pages/DashboardPage";
import Footer from "./components/Footer";
import Header from "./components/Header";
import LandingPage from "./pages/LandingPage";
import LoginForm from "./forms/LoginForm";
import LogoutPage from "./pages/LogoutPage";
import PrivacyPage from "./pages/PrivacyPage";
import TermsPage from "./pages/TermsPage";

const fetch = self.fetch;


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {user: {}};
  }

  componentDidMount() {
    fetch(this.props.apiUrl)
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        if (!_.isEmpty(data.user)) {
          this.setState({user: data.user});
        }
      });
  }

  render() {
    return (
      <div id="readthestuff">
        {!_.isEmpty(this.state.user) ? <Header user={this.state.user} /> : ""}
        <RouteHandler {...this.props} />
        <Footer />
      </div>
    );
  }
}

App.displayName = "ReadTheStuff";
App.propTypes = {
  apiUrl: PropTypes.string.isRequired
};


export default {
  React: React,
  run: function (element, apiUrl) {
    var routes = (
      <Route handler={App} name="app" path="/">
        <DefaultRoute handler={LandingPage} name="landing" />

        <Route handler={LoginForm} name="login-form" path="login" />
        <Route handler={LogoutPage} name="logout" />

        <Route handler={AboutPage} name="about" />
        <Route handler={ContactPage} name="contact" />
        <Route handler={PrivacyPage} name="privacy" />
        <Route handler={TermsPage} name="terms" />

        <Route handler={DashboardPage} name="dashboard" />
      </Route>
    );

    var router = Router.create({
      location: Router.HistoryLocation,
      routes: routes
    });
    router.run(function (Handler) {
      React.render(<Handler apiUrl={apiUrl} />, element);
    });
  }
}
