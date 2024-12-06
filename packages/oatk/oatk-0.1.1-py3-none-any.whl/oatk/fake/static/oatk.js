(function(globals) {

  // As the whole flow is asynchronous and we go back and forth to the OAuth
  // server, and a user might reload the application, we cache the intermediate
  // steps in localStorage.

  // two helper functions to reduce code ;-)
  function save(name, value) {
    window.localStorage.setItem(name, JSON.stringify(value));
    return value;
  }

  function load(name) {
    return JSON.parse(window.localStorage.getItem(name));
  }

  function clear(name) {
    save(name, null);
  }

  // private state

  // The flow consists of getting three things:
  // 1. the URLs to use
  // 2. an authorization code (basiclaly a substitute for the username/password)
  // 3. an access token to actually access resources on behalf of the user

  var urls  = load("oauth_url"),
      code  = load("oauth_code"),
      token = load("oauth_token");

  // We might be called from a redirect after login by the user.
  // Try to extract code from URL.
  // TODO:
  var queryString = window.location.search,
    urlParams = new URLSearchParams(queryString),
    new_code = urlParams.get("code");

  if (new_code && new_code != code) {
    console.log("got new code", new_code, "previous code", code);
    code = save("oauth_code", new_code);
    // reset token, since we got a different new code, triggering getting it
    token = clear("oauth_token");
  }

  // URLs

  const well_known_url = "http://localhost:5000/oauth/well-known";

  function get_urls() {
    console.log("getting urls...");
    // get well-known to bootstrap
    $.getJSON(well_known_url, function(result) {
      urls = save("oauth_url", result);
      console.log("got urls!")
      flow();
    });
  }

  // CODE

  const client_id = "test";

  function randomString(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (var i = 0; i < length; i++) {
      text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
  }

  const nonce = randomString(),
        state = randomString();

  var code_challenge = load("oauth_code_challenge"),
      code_verifier  = load("oauth_code_verifier");


  function dec2hex(dec) {
    return ('0' + dec.toString(16)).substr(-2)
  }

  function generateRandomString() {
    var array = new Uint32Array(56 / 2);
    window.crypto.getRandomValues(array);
    r = Array.from(array, dec2hex).join('');
    return r;
  }

  function base64urlencode(a) {
    var str = "";
    var bytes = new Uint8Array(a);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
      str += String.fromCharCode(bytes[i]);
    }
    return btoa(str)
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=+$/, "");
  }

  function challenge_from_verifier(v) {
    hashed = sha256(v);
    base64encoded = base64urlencode(hashed);
    // console.log(v, hashed.hex(), hashed, base64encoded);
    return base64encoded;
  }

  if (!code_challenge || !code_verifier) {
    code_verifier = save("oauth_code_verificer",  generateRandomString());
    code_challenge = save("oauth_code_challenge", challenge_from_verifier(code_verifier));
  }

  // console.log(code_verifier, code_challenge);

  function get_code() {
    console.log("getting code...");
    // goto auth point, in the end we're redirected here with a ?code=... arg
    window.location.href = urls["authorization_endpoint"] +
      "?client_id=" + client_id +
      "&redirect_uri=" + window.location +
      "&response_type=code" +
      "&response_mode=fragment" +
      "&scope=openid profile" +
      "&state=" + state +
      "&nonce=" + nonce +
      "&code_challenge=" + code_challenge,
      "&code_challenge_method=S256"
  }

  // TOKEN

  function get_token() {
    console.log("getting token...");
    // exchange code for access_token
    $.ajax({
      type: "POST",
      url: urls["token_endpoint"],
      data: JSON.stringify({
        code: code,
        grant_type: "authorization_code",
        client_id: client_id,
        redirect_uri: window.location,
        code_verifier: code_verifier
      }),
      success: function(response) {
        token = save("oauth_token", response.access_token);
        console.log("got token", parseJwt(token));
        flow();
      },
      contentType: "application/json",
      dataType: "json"
    });
  }

  function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
      return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
  };

  // example protected API call

  function get_userinfo() {
    // get userinfo, using the access_token
    $.ajax({
      type: "GET",
      url: urls["userinfo_endpoint"],
      headers: {
        "Authorization": "Bearer " + token
      },
      success: function(response) {
        console.log(response);
      },
      dataType: "json"
    });
  }

  // Public API

  // we expose one function to the application, which triggers the entire flow
  // and results in a user object and an http module with functions to get, 
  // post, put and delete remote resources, adding the required authentication.
  var user = {
      "name": "todo"
    }, // TODO
    http = {
      "getJSON": function(url, on_success) {
        $.ajax({
          type: "GET",
          url: url,
          headers: {
            "Authorization": "Bearer " + token
          },
          success: on_success,
          dataType: "json"
        });
      }
    },
    logout = function() {
      // clear locals
      clear("oauth_code");
      clear("oauth_token");
      // goto logout endpoint
      window.location.href = urls["end_session_endpoint"] +
        "?client_id=" + client_id +
        "&redirect_uri=" + window.location;
    },
    callback = null;

  // exposed function
  var with_authenticated_user = function with_authenicated_user(on_success) {
    callback = on_success;
    flow(); // start flow
  }

  function flow() {
    if (!urls) {
      return get_urls();
    }
    console.log("✅ URLs");
    if (!code) {
      return get_code();
    }
    console.log("✅ authorization code");
    if (!token) {
      return get_token();
    }
    console.log("✅ access token");
    if (!callback) {
      return alert("no callback?!");
    }

    // we've got everyting...
    callback(user, http, logout);
  }

  globals.oatk = {
    "with_authenticated_user": with_authenticated_user
  };


  // helper
  
  /*
  Copyright 2022 Andrea Griffini

  Permission is hereby granted, free of charge, to any person obtaining
  a copy of this software and associated documentation files (the
  "Software"), to deal in the Software without restriction, including
  without limitation the rights to use, copy, modify, merge, publish,
  distribute, sublicense, and/or sell copies of the Software, and to
  permit persons to whom the Software is furnished to do so, subject to
  the following conditions:

  The above copyright notice and this permission notice shall be
  included in all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  */

  // sha256(data) returns the digest
  // sha256() returns an object you can call .add(data) zero or more time and .digest() at the end
  // digest is a 32-byte Uint8Array instance with an added .hex() function.
  // Input should be either a string (that will be encoded as UTF-8) or an array-like object with values 0..255.
  function sha256(data) {
      let h0 = 0x6a09e667, h1 = 0xbb67ae85, h2 = 0x3c6ef372, h3 = 0xa54ff53a,
          h4 = 0x510e527f, h5 = 0x9b05688c, h6 = 0x1f83d9ab, h7 = 0x5be0cd19,
          tsz = 0, bp = 0;
      const k = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                 0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                 0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2],
            rrot = (x, n) => (x >>> n) | (x << (32-n)),
            w = new Uint32Array(64),
            buf = new Uint8Array(64),
            process = () => {
                for (let j=0,r=0; j<16; j++,r+=4) {
                    w[j] = (buf[r]<<24) | (buf[r+1]<<16) | (buf[r+2]<<8) | buf[r+3];
                }
                for (let j=16; j<64; j++) {
                    let s0 = rrot(w[j-15], 7) ^ rrot(w[j-15], 18) ^ (w[j-15] >>> 3);
                    let s1 = rrot(w[j-2], 17) ^ rrot(w[j-2], 19) ^ (w[j-2] >>> 10);
                    w[j] = (w[j-16] + s0 + w[j-7] + s1) | 0;
                }
                let a = h0, b = h1, c = h2, d = h3, e = h4, f = h5, g = h6, h = h7;
                for (let j=0; j<64; j++) {
                    let S1 = rrot(e, 6) ^ rrot(e, 11) ^ rrot(e, 25),
                        ch = (e & f) ^ ((~e) & g),
                        t1 = (h + S1 + ch + k[j] + w[j]) | 0,
                        S0 = rrot(a, 2) ^ rrot(a, 13) ^ rrot(a, 22),
                        maj = (a & b) ^ (a & c) ^ (b & c),
                        t2 = (S0 + maj) | 0;
                    h = g; g = f; f = e; e = (d + t1)|0; d = c; c = b; b = a; a = (t1 + t2)|0;
                }
                h0 = (h0 + a)|0; h1 = (h1 + b)|0; h2 = (h2 + c)|0; h3 = (h3 + d)|0;
                h4 = (h4 + e)|0; h5 = (h5 + f)|0; h6 = (h6 + g)|0; h7 = (h7 + h)|0;
                bp = 0;
            },
            add = data => {
                if (typeof data === "string") {
                    data = (new TextEncoder).encode(data);
                }
                for (let i=0; i<data.length; i++) {
                    buf[bp++] = data[i];
                    if (bp === 64) process();
                }
                tsz += data.length;
            },
            digest = () => {
                buf[bp++] = 0x80; if (bp == 64) process();
                if (bp + 8 > 64) {
                    while (bp < 64) buf[bp++] = 0x00;
                    process();
                }
                while (bp < 58) buf[bp++] = 0x00;
                // Max number of bytes is 35,184,372,088,831
                let L = tsz * 8;
                buf[bp++] = (L / 1099511627776.) & 255;
                buf[bp++] = (L / 4294967296.) & 255;
                buf[bp++] = L >>> 24;
                buf[bp++] = (L >>> 16) & 255;
                buf[bp++] = (L >>> 8) & 255;
                buf[bp++] = L & 255;
                process();
                let reply = new Uint8Array(32);
                reply[ 0] = h0 >>> 24; reply[ 1] = (h0 >>> 16) & 255; reply[ 2] = (h0 >>> 8) & 255; reply[ 3] = h0 & 255;
                reply[ 4] = h1 >>> 24; reply[ 5] = (h1 >>> 16) & 255; reply[ 6] = (h1 >>> 8) & 255; reply[ 7] = h1 & 255;
                reply[ 8] = h2 >>> 24; reply[ 9] = (h2 >>> 16) & 255; reply[10] = (h2 >>> 8) & 255; reply[11] = h2 & 255;
                reply[12] = h3 >>> 24; reply[13] = (h3 >>> 16) & 255; reply[14] = (h3 >>> 8) & 255; reply[15] = h3 & 255;
                reply[16] = h4 >>> 24; reply[17] = (h4 >>> 16) & 255; reply[18] = (h4 >>> 8) & 255; reply[19] = h4 & 255;
                reply[20] = h5 >>> 24; reply[21] = (h5 >>> 16) & 255; reply[22] = (h5 >>> 8) & 255; reply[23] = h5 & 255;
                reply[24] = h6 >>> 24; reply[25] = (h6 >>> 16) & 255; reply[26] = (h6 >>> 8) & 255; reply[27] = h6 & 255;
                reply[28] = h7 >>> 24; reply[29] = (h7 >>> 16) & 255; reply[30] = (h7 >>> 8) & 255; reply[31] = h7 & 255;
                reply.hex = () => {
                    let res = "";
                    reply.forEach(x => res += ("0" + x.toString(16)).slice(-2));
                    return res;
                };
                return reply;
            };
      if (data === undefined) return {add, digest};
      add(data);
      return digest();
  }

})(window);
