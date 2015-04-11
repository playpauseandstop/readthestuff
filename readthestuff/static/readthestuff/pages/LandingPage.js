/**
 * Landing Page
 * ============
 *
 * Default page for unathorized users.
 *
 */

"use strict";

import React from "react";
import { Link } from "react-router";


class LandingPage extends React.Component {
  render() {
    return (
      <div className="container container-main">
        <div className="row">
          <div className="col-xs-12 col-sm-10 col-sm-offset-1">
            <h2>Like Google Reader</h2>
            <p>
              <em>Read</em> <strong>all</strong> updates from your feeds, like
              you want, not like system decides for you.
            </p>
            <p>
              <em>Keep</em> and <em>share</em> entries in
              your <a href="https://www.dropbox.com/">Dropbox</a> or across
              your social networks,
              like <a href="https://www.facebook.com/">Facebook</a> or <a href="https://twitter.com/">Twitter</a>.
            </p>
          </div>
        </div>

        <div className="row">
          <div className="col-xs-12 col-sm-10 col-sm-offset-1">
            <h2>But still working</h2>
            <p>
              To start all you need to log into with one of your Google,
              Dropbox, Facebook, or Twitter account and import your feeds from
              OPML file or add them via UI.
            </p>
            <p>
              Built on top
              of <a href="https://www.python.org/">Python 3</a> &amp; <a href="https://asyncio.org/">Asyncio
              stack</a> on backend and with <a href="https://facebook.github.io/react">React.js</a> on
              frontend, <em>Read the Stuff</em> is an open-source project, which could be modified by
              you! Follow us on <a href="https://github.com/playpauseandstop/readthestuff">GitHub</a> and
              make web better, together!
            </p>
          </div>
        </div>

        <div className="row">
          <div className="col-xs-12 col-sm-10 col-sm-offset-1">
            <h2>And more</h2>
            <p>
              <em>Read the Stuff</em> built with mobility in mind, so it
              perfectly works and looks on mobiles and tables (thanks
              to <a href="https://getbootstrap.com/">Bootstrap</a>) and
              supports offline mode to continue read feed entries without
              Internet connection.
            </p>
            <p>
              You will able to export all you data (not only subscribed feeds,
              but also saved & shared entries) anytime you want.
            </p>
            <p>
              We are open for your ideas to make Read the Stuff better! Send
              your feature and pull requests
              on <a href="https://github.com/playpauseandstop/readthestuff">GitHub</a> and
              we together will build modern feed reader for modern web.
            </p>
          </div>
        </div>
      </div>
    );
  }
}

LandingPage.displayName = "Landing Page";


export default LandingPage;
