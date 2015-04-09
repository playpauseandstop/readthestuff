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
      <div>
        Hello, world!
      </div>
    );
  }
}

LandingPage.displayName = "Landing Page";


export default LandingPage;
