/* Theme 03 interactive engine - vanilla JS + canvas, on-brand (dark teal).
   Each mount: <div class="iact" data-widget="..." data-json="..."></div>
   Data comes from assets/data/theme3_*.json (real, verified values). */
(function () {
  "use strict";
  var C = {
    teal1: "#052e36", teal3: "#0d5963", teal4: "#15616d",
    gold: "#c8a05c", goldL: "#e7c98a", green: "#6dd9a1",
    clay: "#c44a30", cream: "#f3ecd6", muted: "#a8b5b8", sky: "#7fb3bd",
    grid: "rgba(199,160,92,0.18)"
  };
  var DPR = Math.max(1, window.devicePixelRatio || 1);

  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }
  function fmt(x, d) { if (x == null || isNaN(x)) return "-"; d = d == null ? 2 : d; return Math.abs(x) >= 1000 ? Math.round(x).toLocaleString() : (+x).toFixed(d); }
  function lerp(a, b, t) { return a + (b - a) * t; }
  function nearest(arr, v) { var best = arr[0], bd = Infinity; arr.forEach(function (x) { var dd = Math.abs(x - v); if (dd < bd) { bd = dd; best = x; } }); return best; }

  // hi-dpi canvas sized to its CSS box
  function mkCanvas(parent, h) {
    var c = el("canvas", "iact-canvas"); c.style.width = "100%"; c.style.height = h + "px";
    parent.appendChild(c);
    function size() { var w = c.clientWidth || parent.clientWidth || 600; c.width = w * DPR; c.height = h * DPR; }
    size(); window.addEventListener("resize", function () { size(); if (c._draw) c._draw(); });
    return c;
  }
  function ctxOf(c) { var x = c.getContext("2d"); x.setTransform(DPR, 0, 0, DPR, 0, 0); return x; }

  // generic scatter with linear axes; returns helpers for hit-testing
  function scatterAxes(x, W, H, xr, yr, pad) {
    pad = pad || { l: 52, r: 16, t: 16, b: 40 };
    var px = function (v) { return lerp(pad.l, W - pad.r, (v - xr[0]) / (xr[1] - xr[0] || 1)); };
    var py = function (v) { return lerp(H - pad.b, pad.t, (v - yr[0]) / (yr[1] - yr[0] || 1)); };
    x.clearRect(0, 0, W, H);
    x.strokeStyle = C.grid; x.fillStyle = C.cream; x.lineWidth = 1; x.font = "11px 'DM Sans',sans-serif";
    var i, t;
    for (i = 0; i <= 4; i++) {
      t = i / 4; var gy = lerp(H - pad.b, pad.t, t), gx = lerp(pad.l, W - pad.r, t);
      x.beginPath(); x.moveTo(pad.l, gy); x.lineTo(W - pad.r, gy); x.stroke();
      x.fillStyle = C.muted; x.textAlign = "right"; x.fillText(fmt(lerp(yr[0], yr[1], t), 2), pad.l - 6, gy + 3);
      x.textAlign = "center"; x.fillText(fmt(lerp(xr[0], xr[1], t), 2), gx, H - pad.b + 16);
    }
    return { px: px, py: py, pad: pad };
  }

  function chip(label, active) { var b = el("button", "iact-chip" + (active ? " on" : ""), label); return b; }
  function dropdown(opts, val) {
    var s = el("select", "iact-sel");
    opts.forEach(function (o) { var op = el("option", null, o.label); op.value = o.value; if (o.value === val) op.selected = true; s.appendChild(op); });
    return s;
  }
  function header(mount, title, sub) {
    var h = el("div", "iact-head");
    h.appendChild(el("span", "iact-ttl", title));
    if (sub) h.appendChild(el("span", "iact-sub", sub));
    mount.appendChild(h); return h;
  }

  /* ---------- A. MORPH STUDIO: slider morphs spheroid + redraws curves ---------- */
  function morphStudio(mount, d) {
    header(mount, "Tune the simulator", "drag a knob, watch the spheroid and its cluster size respond");
    var keys = Object.keys(d.params);
    var cur = keys.indexOf("width") >= 0 ? "width" : keys[0];
    var feat = "total_area";
    var bar = el("div", "iact-controls"); mount.appendChild(bar);
    var segWrap = el("div", "iact-seg"); bar.appendChild(segWrap);
    var featSel = dropdown((d.meta.primary_features || ["total_area", "circularity", "solidity"]).map(function (f) { return { value: f, label: (d.meta.feature_labels || {})[f] || f }; }), feat);
    var featLbl = el("label", "iact-field"); featLbl.appendChild(el("span", "iact-flab", "curve")); featLbl.appendChild(featSel); bar.appendChild(featLbl);

    var grid = el("div", "iact-2col"); mount.appendChild(grid);
    var left = el("div", "iact-stage"); grid.appendChild(left);
    var img = el("img", "iact-spheroid"); img.alt = "rendered synthetic spheroid"; left.appendChild(img);
    var cap = el("div", "iact-cap"); left.appendChild(cap);
    var right = el("div"); grid.appendChild(right);
    var canvas = mkCanvas(right, 240);
    var read = el("div", "iact-readout"); right.appendChild(read);

    var sliderWrap = el("div", "iact-slider"); mount.appendChild(sliderWrap);
    var slider = el("input"); slider.type = "range"; sliderWrap.appendChild(slider);
    var ticks = el("div", "iact-ticks"); mount.appendChild(ticks);

    function segButtons() {
      segWrap.innerHTML = "";
      keys.forEach(function (k) {
        var b = chip(d.params[k].label, k === cur);
        b.onclick = function () { cur = k; setup(); };
        segWrap.appendChild(b);
      });
    }
    var idx = 0;
    function setup() {
      segButtons();
      var p = d.params[cur];
      slider.min = 0; slider.max = p.levels.length - 1; slider.step = 1;
      idx = p.levels.indexOf(p.default_level); if (idx < 0) idx = Math.floor(p.levels.length / 2);
      slider.value = idx;
      ticks.innerHTML = "";
      p.levels.forEach(function (lv, i) { var t = el("span", "iact-tick" + (i === idx ? " on" : ""), String(lv)); ticks.appendChild(t); });
      draw();
    }
    function frameFor(p, level) {
      if (!p.frames || !p.frames.length) return null;
      var fl = p.frame_levels || p.frames.map(function (f) { return f.level; });
      var nl = nearest(fl, level);
      var hit = p.frames.filter(function (f) { return f.level === nl; })[0];
      return hit ? { src: hit.src, level: nl, exact: nl === level } : null;
    }
    function draw() {
      var p = d.params[cur]; idx = +slider.value; var level = p.levels[idx];
      Array.prototype.forEach.call(ticks.children, function (t, i) { t.className = "iact-tick" + (i === idx ? " on" : ""); });
      var fr = frameFor(p, level);
      if (fr) { img.style.display = ""; img.src = fr.src; cap.textContent = fr.exact ? (p.label + " = " + level) : (p.label + " = " + level + "  (nearest render: " + fr.level + ")"); }
      else { img.style.display = "none"; cap.textContent = p.label + " = " + level; }
      // curve
      var F = p.features[feat]; var x = ctxOf(canvas), W = canvas.clientWidth, H = 240;
      var xr = [p.levels[0], p.levels[p.levels.length - 1]];
      var ys = F.mean.slice(); var lo = ys.map(function (m, i) { return m - (F.std ? F.std[i] : 0); }); var hi = ys.map(function (m, i) { return m + (F.std ? F.std[i] : 0); });
      var ymin = Math.min.apply(null, lo), ymax = Math.max.apply(null, hi); var padv = (ymax - ymin) * 0.08 || 1;
      var ax = scatterAxes(x, W, H, xr, [ymin - padv, ymax + padv]);
      // band
      x.beginPath();
      p.levels.forEach(function (lv, i) { var X = ax.px(lv), Y = ax.py(hi[i]); i ? x.lineTo(X, Y) : x.moveTo(X, Y); });
      for (var i = p.levels.length - 1; i >= 0; i--) { x.lineTo(ax.px(p.levels[i]), ax.py(lo[i])); }
      x.closePath(); x.fillStyle = "rgba(200,160,92,0.16)"; x.fill();
      // mean line
      x.beginPath(); x.lineWidth = 2; x.strokeStyle = C.gold;
      p.levels.forEach(function (lv, i) { var X = ax.px(lv), Y = ax.py(ys[i]); i ? x.lineTo(X, Y) : x.moveTo(X, Y); });
      x.stroke();
      // current marker
      var cx = ax.px(level), cy = ax.py(ys[idx]);
      x.beginPath(); x.arc(cx, cy, 6, 0, 7); x.fillStyle = C.green; x.fill(); x.lineWidth = 2; x.strokeStyle = C.cream; x.stroke();
      x.fillStyle = C.muted; x.textAlign = "center"; x.font = "11px 'DM Sans'"; x.fillText((d.meta.feature_labels || {})[feat] || feat, W / 2, 12);
      read.innerHTML = "<b>" + (d.meta.feature_labels || {})[feat] + "</b> at " + p.label + " " + level + ": <b style='color:" + C.goldL + "'>" + fmt(ys[idx], feat === "total_area" ? 0 : 3) + "</b>";
      canvas._draw = draw;
    }
    featSel.onchange = function () { feat = featSel.value; draw(); };
    slider.oninput = draw;
    setup();
  }

  /* ---------- B. MORPHOSPACE EXPLORER: clickable 1105-sample cloud ---------- */
  function morphospace(mount, d) {
    header(mount, "Explore the simulation library", "every point is one of 1,105 synthetic spheroids - click to read its 7 CPM knobs");
    var feats = d.meta.features, pLabels = d.meta.params;
    var ax1 = (d.meta.default_axes && d.meta.default_axes[0]) || "total_area";
    var ay1 = (d.meta.default_axes && d.meta.default_axes[1]) || "circularity";
    var colorBy = d.meta.default_color || "contact";
    var bar = el("div", "iact-controls"); mount.appendChild(bar);
    function field(lbl, sel) { var f = el("label", "iact-field"); f.appendChild(el("span", "iact-flab", lbl)); f.appendChild(sel); bar.appendChild(f); return f; }
    var fopts = feats.map(function (f) { return { value: f, label: f.replace(/_/g, " ") }; });
    var popts = pLabels.map(function (p) { return { value: p, label: p.replace(/_/g, " ") }; });
    var selX = dropdown(fopts, ax1), selY = dropdown(fopts, ay1), selC = dropdown(popts, colorBy);
    field("x", selX); field("y", selY); field("colour", selC);
    var exBtn = chip("highlight extremes", false); bar.appendChild(exBtn);
    var exRow = el("div", "iact-seg"); exRow.style.flexBasis = "100%"; exRow.style.marginTop = "0.2rem"; bar.appendChild(exRow);
    var EXLAB = { max_area: "max area", min_area: "min area", max_circularity: "max circularity", min_circularity: "min circularity" };

    var grid = el("div", "iact-2col"); mount.appendChild(grid);
    var cwrap = el("div"); grid.appendChild(cwrap);
    var canvas = mkCanvas(cwrap, 360);
    var card = el("div", "iact-card"); grid.appendChild(card);
    card.innerHTML = "<div class='iact-hint'>Click any point. Outlined points have a rendered spheroid.</div>";
    var leg = el("div", "iact-readout"); leg.style.marginTop = "0.4rem";
    leg.innerHTML = "<span style='color:#f3ecd6'>&#9711; outlined</span> = has a rendered spheroid (click to view) &nbsp;&middot;&nbsp; <span style='opacity:.45'>faded</span> = parameters only";
    cwrap.appendChild(leg);

    var pts = d.points, exIds = [], exImg = {};
    if (d.extremes) Object.keys(d.extremes).forEach(function (k) { var v = d.extremes[k]; var id = typeof v === "object" ? v.sample_id : v; exIds.push(id); if (v && v.img) exImg[id] = v.img; });
    function hasRender(p) { var S = d.meta.spheroids; return !!(S && p.sample_id >= S.min && p.sample_id <= S.max); }
    var showEx = false, screen = [];
    function rng(key) { var lo = Infinity, hi = -Infinity; pts.forEach(function (p) { lo = Math.min(lo, p[key]); hi = Math.max(hi, p[key]); }); return [lo, hi]; }
    function colorFor(v, r) { var t = (v - r[0]) / (r[1] - r[0] || 1); return "rgb(" + Math.round(lerp(125, 231, t)) + "," + Math.round(lerp(179, 200, t)) + "," + Math.round(lerp(189, 124, t)) + ")"; }
    var sel = null;
    function draw() {
      var x = ctxOf(canvas), W = canvas.clientWidth, H = 360;
      var xr = rng(selX.value), yr = rng(selY.value), cr = rng(selC.value);
      var a = scatterAxes(x, W, H, xr, yr); screen = [];
      pts.forEach(function (p) {
        var X = a.px(p[selX.value]), Y = a.py(p[selY.value]); screen.push({ X: X, Y: Y, p: p });
        var ex = showEx && exIds.indexOf(p.sample_id) >= 0, rend = hasRender(p);
        x.beginPath(); x.arc(X, Y, ex ? 6 : rend ? 3.5 : 2.4, 0, 7);
        x.fillStyle = ex ? C.clay : colorFor(p[selC.value], cr);
        x.globalAlpha = ex ? 1 : rend ? 0.92 : 0.26; x.fill(); x.globalAlpha = 1;
        if (ex) { x.lineWidth = 1.5; x.strokeStyle = C.cream; x.stroke(); }
        else if (rend) { x.lineWidth = 1; x.strokeStyle = "rgba(243,236,214,0.85)"; x.stroke(); }
      });
      if (sel) { x.beginPath(); x.arc(a.px(sel[selX.value]), a.py(sel[selY.value]), 7, 0, 7); x.strokeStyle = C.goldL; x.lineWidth = 2.5; x.stroke(); }
      x.fillStyle = C.muted; x.font = "11px 'DM Sans'"; x.textAlign = "center";
      x.fillText(selX.value.replace(/_/g, " "), W / 2, H - 6);
      x.save(); x.translate(12, H / 2); x.rotate(-Math.PI / 2); x.fillText(selY.value.replace(/_/g, " "), 0, 0); x.restore();
      canvas._draw = draw;
    }
    function showCard(p) {
      var ph = "<div class='iact-cardh'>Sample #" + p.sample_id + (exIds.indexOf(p.sample_id) >= 0 ? " <span class='iact-badge'>extreme</span>" : "") + "</div>";
      var imgsrc = exImg[p.sample_id];
      if (!imgsrc && d.meta.spheroids) { var S = d.meta.spheroids; if (p.sample_id >= S.min && p.sample_id <= S.max) imgsrc = S.path.replace("{id}", p.sample_id); }
      if (imgsrc) ph += "<img class='iact-spheroid' style='margin-bottom:0.7rem' src='" + imgsrc + "' onerror=\"this.style.display='none'\" alt='rendered spheroid for sample " + p.sample_id + "'>";
      var rows = "<div class='iact-kv'><div class='iact-kvg'>CPM parameters</div>";
      pLabels.forEach(function (k) { rows += "<div><span>" + k.replace(/_/g, " ") + "</span><b>" + fmt(p[k], 2) + "</b></div>"; });
      rows += "</div><div class='iact-kv'><div class='iact-kvg'>resulting morphology</div>";
      feats.forEach(function (k) { rows += "<div><span>" + k.replace(/_/g, " ") + "</span><b>" + fmt(p[k], k === "total_area" || k === "perimeter" || k === "equivalent_diameter" ? 0 : 3) + "</b></div>"; });
      rows += "</div>";
      card.innerHTML = ph + rows;
    }
    canvas.addEventListener("click", function (e) {
      var r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top, best = null, bd = 1600;
      screen.forEach(function (s) { var dd = (s.X - mx) * (s.X - mx) + (s.Y - my) * (s.Y - my); if (dd < bd) { bd = dd; best = s.p; } });
      if (best) { sel = best; showCard(best); draw(); }
    });
    selX.onchange = selY.onchange = selC.onchange = draw;
    exBtn.onclick = function () {
      showEx = !showEx; exBtn.classList.toggle("on", showEx); exRow.innerHTML = "";
      if (showEx && d.extremes) {
        Object.keys(d.extremes).forEach(function (k) {
          var id = typeof d.extremes[k] === "object" ? d.extremes[k].sample_id : d.extremes[k];
          var b = chip((EXLAB[k] || k.replace(/_/g, " ")) + " #" + id, false);
          b.onclick = function () { var p = pts.filter(function (q) { return q.sample_id === id; })[0]; if (p) { sel = p; showCard(p); draw(); } };
          exRow.appendChild(b);
        });
      }
      draw();
    };
    if (d.meta.extremes_image) { var ei = el("img", "iact-extimg"); ei.src = d.meta.extremes_image; ei.alt = "morphology extremes"; mount.appendChild(ei); }
    draw();
  }

  /* ---------- C. COVERAGE: real wells vs synthetic library, threshold slider ---------- */
  function coverage(mount, d) {
    header(mount, "Does the simulator cover reality?", "real spheroids (coloured) overlaid on the synthetic library (grey) in PCA space");
    var ve = d.meta.pca_variance_explained || [0, 0];
    var grid = el("div", "iact-2col"); mount.appendChild(grid);
    var cwrap = el("div"); grid.appendChild(cwrap);
    var canvas = mkCanvas(cwrap, 360);
    var side = el("div"); grid.appendChild(side);
    var kpi = el("div", "iact-bigstat"); side.appendChild(kpi);
    var note = el("div", "iact-readout"); side.appendChild(note);
    note.innerHTML = "Drag the threshold: a real well counts as <b>outside the library</b> when its nearest-synthetic distance exceeds it.";
    var sw = el("div", "iact-slider"); mount.appendChild(sw);
    var lab = el("div", "iact-flab"); lab.textContent = "out-of-library threshold (nearest-neighbour distance)"; mount.appendChild(lab);
    var slider = el("input"); slider.type = "range"; slider.min = 0; slider.max = 1; slider.step = 0.001;
    slider.value = d.synth_nn.p95 != null ? d.synth_nn.p95 : 0.3; sw.appendChild(slider);

    var allx = d.synthetic_points.map(function (p) { return p.pc1; }).concat(d.real_wells.map(function (p) { return p.pc1; }));
    var ally = d.synthetic_points.map(function (p) { return p.pc2; }).concat(d.real_wells.map(function (p) { return p.pc2; }));
    var xr = [Math.min.apply(null, allx), Math.max.apply(null, allx)], yr = [Math.min.apply(null, ally), Math.max.apply(null, ally)];
    slider.min = d.real_nn_min; slider.max = d.real_nn_max;
    function draw() {
      var thr = +slider.value, x = ctxOf(canvas), W = canvas.clientWidth, H = 360;
      var a = scatterAxes(x, W, H, xr, yr);
      d.synthetic_points.forEach(function (p) { x.beginPath(); x.arc(a.px(p.pc1), a.py(p.pc2), 2.5, 0, 7); x.fillStyle = "rgba(168,181,184,0.35)"; x.fill(); });
      var out = 0;
      d.real_wells.forEach(function (p) { var o = p.nn_distance > thr; if (o) out++; x.beginPath(); x.arc(a.px(p.pc1), a.py(p.pc2), 3.5, 0, 7); x.fillStyle = o ? C.clay : C.green; x.globalAlpha = 0.85; x.fill(); x.globalAlpha = 1; });
      x.fillStyle = C.muted; x.font = "11px 'DM Sans'"; x.textAlign = "center";
      x.fillText("PC1 (" + Math.round(ve[0] * 100) + "% var)", W / 2, H - 6);
      x.save(); x.translate(12, H / 2); x.rotate(-Math.PI / 2); x.fillText("PC2 (" + Math.round(ve[1] * 100) + "% var)", 0, 0); x.restore();
      var pct = (100 * out / d.real_wells.length).toFixed(0);
      kpi.innerHTML = "<div class='iact-bignum'>" + out + " / " + d.real_wells.length + "</div><div class='iact-biglab'>real wells outside the library (" + pct + "%) at distance &gt; " + thr.toFixed(2) + "</div>";
      canvas._draw = draw;
    }
    slider.oninput = draw; draw();
  }

  /* ---------- D. SURROGATE: XGBoost R2 + Sobol toggle ---------- */
  function surrogate(mount, d) {
    header(mount, "The XGBoost surrogate", d.meta.surrogate_config || "gradient-boosted trees, 5-fold CV");
    var tabs = el("div", "iact-seg"); mount.appendChild(tabs);
    var t1 = chip("How well can it predict?", true), t2 = chip("What drives each feature?", false);
    tabs.appendChild(t1); tabs.appendChild(t2);
    var body = el("div"); mount.appendChild(body);
    var mode = "r2", metric = "ST", selFeat = null;
    function setTab(m) { mode = m; t1.classList.toggle("on", m === "r2"); t2.classList.toggle("on", m === "sobol"); render(); }
    t1.onclick = function () { setTab("r2"); }; t2.onclick = function () { setTab("sobol"); };
    function render() {
      body.innerHTML = "";
      if (mode === "r2") {
        body.appendChild(el("div", "iact-readout", "Cross-validated R&sup2; per shape feature. Click a bar to see its 5 folds. <b>Circularity</b> is near-perfect; <b>eccentricity</b> is the weak link."));
        var c = mkCanvas(body, 36 * d.r2_bars.length + 30);
        var det = el("div", "iact-readout"); body.appendChild(det);
        var draw = function () {
          var x = ctxOf(c), W = c.clientWidth, H = c.clientHeight / DPR, padL = 120, padR = 54, rows = d.r2_bars.length, bh = (H - 20) / rows;
          x.clearRect(0, 0, W, H);
          d.r2_bars.forEach(function (b, i) {
            var y = 10 + i * bh, w = (W - padL - padR) * Math.max(0, b.cv_r2_mean);
            x.fillStyle = b.feature === selFeat ? C.goldL : C.gold; x.fillRect(padL, y + bh * 0.18, w, bh * 0.5);
            x.fillStyle = C.cream; x.font = "12px 'DM Sans'"; x.textAlign = "right"; x.fillText(b.label, padL - 8, y + bh * 0.5);
            x.textAlign = "left"; x.fillStyle = C.goldL; x.fillText("R² " + b.cv_r2_mean.toFixed(2), padL + w + 6, y + bh * 0.5);
          });
          c._draw = draw; c._rows = { padL: padL, bh: bh };
        };
        draw();
        c.addEventListener("click", function (e) {
          var r = c.getBoundingClientRect(), my = e.clientY - r.top, i = Math.floor((my - 10) / c._rows.bh);
          if (i >= 0 && i < d.r2_bars.length) { var b = d.r2_bars[i]; selFeat = b.feature; draw(); det.innerHTML = "<b>" + b.label + "</b> folds: " + b.folds.map(function (f) { return f.toFixed(3); }).join(", ") + " &nbsp;|&nbsp; mean R&sup2; " + b.cv_r2_mean.toFixed(3) + " &plusmn; " + b.cv_r2_std.toFixed(3) + " &nbsp;|&nbsp; MAE " + b.mae_pct + "%"; }
        });
      } else {
        var s = d.sobol; var feated = selFeat && s.features.indexOf(selFeat) >= 0 ? selFeat : s.features[0];
        var seg = el("div", "iact-controls"); body.appendChild(seg);
        var fl = dropdown(s.features.map(function (f) { return { value: f, label: f.replace(/_/g, " ") }; }), feated);
        var lf = el("label", "iact-field"); lf.appendChild(el("span", "iact-flab", "feature")); lf.appendChild(fl); seg.appendChild(lf);
        ["S1", "ST", "gap"].forEach(function (m) { var b = chip(m === "S1" ? "direct (S1)" : m === "ST" ? "total (ST)" : "interaction gap", metric === m); b.onclick = function () { metric = m; render(); }; seg.appendChild(b); });
        body.appendChild(el("div", "iact-readout", "How much each knob drives <b>" + feated.replace(/_/g, " ") + "</b>. Big total-vs-direct gap = the knob acts through interactions."));
        var c = mkCanvas(body, 34 * s.parameters.length + 24);
        var fi = s.features.indexOf(feated);
        var vals = s.parameters.map(function (p, j) { var v = metric === "S1" ? s.S1[fi][j] : metric === "ST" ? s.ST[fi][j] : (s.gap ? s.gap[fi][j] : s.ST[fi][j] - s.S1[fi][j]); return { p: p, v: v }; });
        var mx = Math.max.apply(null, vals.map(function (o) { return o.v; })) || 1;
        var draw = function () {
          var x = ctxOf(c), W = c.clientWidth, H = c.clientHeight / DPR, padL = 150, padR = 44, bh = (H - 12) / vals.length;
          x.clearRect(0, 0, W, H);
          vals.forEach(function (o, i) {
            var y = 6 + i * bh, w = (W - padL - padR) * (o.v / mx);
            x.fillStyle = metric === "gap" ? C.clay : C.gold; x.fillRect(padL, y + bh * 0.2, Math.max(0, w), bh * 0.5);
            x.fillStyle = C.cream; x.font = "12px 'DM Sans'"; x.textAlign = "right"; x.fillText(o.p.replace(/_/g, " "), padL - 8, y + bh * 0.5);
            x.textAlign = "left"; x.fillStyle = C.goldL; x.fillText(o.v.toFixed(2), padL + Math.max(0, w) + 6, y + bh * 0.5);
          });
          c._draw = draw;
        };
        draw();
        fl.onchange = function () { selFeat = fl.value; render(); };
      }
    }
    render();
  }

  /* ---------- E. QC THRESHOLD EXPLORER (Theme 01) ---------- */
  function qcthreshold(mount, d) {
    header(mount, "Set your quality bar", "drag the threshold and watch how many of the 12,480 frames survive");
    var M = d.meta.metrics, keys = Object.keys(M), cur = keys[0];
    var bar = el("div", "iact-controls"); mount.appendChild(bar);
    var seg = el("div", "iact-seg"); bar.appendChild(seg);
    var grid = el("div", "iact-2col"); mount.appendChild(grid);
    var cwrap = el("div"); grid.appendChild(cwrap); var canvas = mkCanvas(cwrap, 320);
    var side = el("div"); grid.appendChild(side);
    var kpi = el("div", "iact-bigstat"); side.appendChild(kpi);
    var note = el("div", "iact-readout"); side.appendChild(note);
    var sw = el("div", "iact-slider"); mount.appendChild(sw); var slider = el("input"); slider.type = "range"; sw.appendChild(slider);
    var lab = el("div", "iact-flab"); mount.appendChild(lab);
    var thr;
    function passN(m, t) { var cc = m.count_curve, best = cc[0]; cc.forEach(function (p) { if (Math.abs(p.v - t) < Math.abs(best.v - t)) best = p; }); return best.n; }
    function segBtns() { seg.innerHTML = ""; keys.forEach(function (k) { var b = chip(M[k].label, k === cur); b.onclick = function () { cur = k; setup(); }; seg.appendChild(b); }); }
    function setup() { segBtns(); var m = M[cur]; slider.min = m.min; slider.max = m.max; slider.step = (m.max - m.min) / 200 || 0.001; thr = m.default; slider.value = thr; lab.textContent = m.label + " threshold" + (m.invert ? " (PASS = at or below)" : " (PASS = at or above)"); draw(); }
    function draw() {
      var m = M[cur]; thr = +slider.value; var x = ctxOf(canvas), W = canvas.clientWidth, H = 320;
      var hr = [0, 132]; var yr = [m.min, m.max]; var a = scatterAxes(x, W, H, hr, yr);
      d.points.forEach(function (p) { var v = p[cur]; var pass = m.invert ? v <= thr : v >= thr; x.beginPath(); x.arc(a.px(p.h), a.py(v), 2.4, 0, 7); x.fillStyle = pass ? C.gold : C.clay; x.globalAlpha = pass ? 0.75 : 0.5; x.fill(); x.globalAlpha = 1; });
      var ty = a.py(thr); x.beginPath(); x.setLineDash([5, 4]); x.strokeStyle = C.cream; x.lineWidth = 1.5; x.moveTo(a.pad.l, ty); x.lineTo(W - 16, ty); x.stroke(); x.setLineDash([]);
      x.fillStyle = C.muted; x.font = "11px 'DM Sans'"; x.textAlign = "center"; x.fillText("time (h)", W / 2, H - 6);
      x.save(); x.translate(12, H / 2); x.rotate(-Math.PI / 2); x.fillText(m.label, 0, 0); x.restore();
      var n = passN(m, thr), pct = (100 * n / d.meta.n_total).toFixed(0);
      kpi.innerHTML = "<div class='iact-bignum'>" + n.toLocaleString() + " / " + d.meta.n_total.toLocaleString() + "</div><div class='iact-biglab'>frames pass (" + pct + "%) at " + m.label.toLowerCase() + " " + (m.invert ? "&le; " : "&ge; ") + thr.toFixed(3) + "</div>";
      note.innerHTML = "Gold dots pass your bar, red dots fail. Median " + m.label.toLowerCase() + " is " + m.p50.toFixed(3) + ".";
      canvas._draw = draw;
    }
    slider.oninput = draw; setup();
  }

  /* ---------- F. MODEL EXPLORER (Theme 02) ---------- */
  function modelscatter(mount, d) {
    header(mount, "Pixel overlap vs feature preservation", "click a segmenter: high Dice does not mean trustworthy shape numbers");
    var grid = el("div", "iact-2col"); mount.appendChild(grid);
    var cwrap = el("div"); grid.appendChild(cwrap); var canvas = mkCanvas(cwrap, 360);
    var card = el("div", "iact-card"); grid.appendChild(card); card.innerHTML = "<div class='iact-hint'>Click a model point.</div>";
    var xr = [d.meta.x_axis.min, d.meta.x_axis.max], yr = [d.meta.y_axis.min, d.meta.y_axis.max], screen = [], sel = null;
    function draw() {
      var x = ctxOf(canvas), W = canvas.clientWidth, H = 360; var a = scatterAxes(x, W, H, xr, yr); screen = [];
      if (d.meta.reliability_bar) { var ry = a.py(d.meta.reliability_bar); x.setLineDash([5, 4]); x.strokeStyle = "rgba(168,181,184,0.5)"; x.beginPath(); x.moveTo(a.pad.l, ry); x.lineTo(W - 16, ry); x.stroke(); x.setLineDash([]); }
      d.points.forEach(function (p) { var X = a.px(p.dice), Y = a.py(p.ccc); screen.push({ X: X, Y: Y, p: p }); x.beginPath(); x.arc(X, Y, p.winner ? 8 : 5, 0, 7); x.fillStyle = p.winner ? C.green : C.gold; x.fill(); if (p === sel) { x.lineWidth = 2.5; x.strokeStyle = C.cream; x.stroke(); } x.fillStyle = C.muted; x.font = "10px 'DM Sans'"; x.textAlign = "left"; x.fillText(p.label, X + 9, Y + 3); });
      x.fillStyle = C.muted; x.font = "11px 'DM Sans'"; x.textAlign = "center"; x.fillText(d.meta.x_axis.label, W / 2, H - 6);
      x.save(); x.translate(12, H / 2); x.rotate(-Math.PI / 2); x.fillText(d.meta.y_axis.label, 0, 0); x.restore();
      canvas._draw = draw;
    }
    function show(p) {
      var h = "<div class='iact-cardh'>" + p.label + (p.winner ? " <span class='iact-badge' style='background:var(--green);color:var(--teal-1)'>chosen</span>" : "") + "</div>";
      var kv = "<div class='iact-kv'><div class='iact-kvg'>overall</div><div><span>Dice (pixel)</span><b>" + fmt(p.dice, 3) + "</b></div><div><span>CC-Dice</span><b>" + fmt(p.cc_dice, 3) + "</b></div><div><span>CCC (shape)</span><b>" + fmt(p.ccc, 3) + "</b></div></div>";
      kv += "<div class='iact-kv'><div class='iact-kvg'>per-feature agreement (CCC)</div>";
      d.meta.features.forEach(function (f) { var v = (p.features_ccc || {})[f]; if (v == null) return; kv += "<div><span>" + f.replace(/_/g, " ") + "</span><b style='color:" + (v >= 0.85 ? C.green : v >= 0.5 ? C.gold : C.clay) + "'>" + fmt(v, 3) + "</b></div>"; });
      kv += "</div>";
      if (p.config && Object.keys(p.config).length) {
        kv += "<div class='iact-kv'><div class='iact-kvg'>training config</div>";
        Object.keys(p.config).forEach(function (k) { kv += "<div><span>" + k.replace(/_/g, " ") + "</span><b>" + p.config[k] + "</b></div>"; });
        kv += "</div>";
      }
      if (p.config_note) kv += "<div class='iact-readout' style='margin-top:0'>" + p.config_note + "</div>";
      card.innerHTML = h + kv;
    }
    canvas.addEventListener("click", function (e) { var r = canvas.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top, best = null, bd = 1600; screen.forEach(function (s) { var dd = (s.X - mx) * (s.X - mx) + (s.Y - my) * (s.Y - my); if (dd < bd) { bd = dd; best = s.p; } }); if (best) { sel = best; show(best); draw(); } });
    draw();
  }

  /* ---------- G. DISCRIMINABILITY HEATMAP (Theme 04) ---------- */
  function heatmap(mount, d) {
    header(mount, "Feature to parameter importance", "which shape numbers carry information about which CPM knob");
    var note = el("div", "iact-readout"); note.innerHTML = "Click a cell to read its importance. Brighter gold = that feature is more informative about that parameter."; mount.appendChild(note);
    var ncol = d.params.length;
    var g = el("div"); g.style.display = "grid"; g.style.gridTemplateColumns = "minmax(96px,1.1fr) repeat(" + ncol + ",1fr)"; g.style.gap = "3px"; g.style.marginTop = "0.8rem"; mount.appendChild(g);
    function cell(txt, cls) { var c = el("div", cls); c.textContent = txt; c.style.padding = "0.5rem 0.3rem"; c.style.fontFamily = "'JetBrains Mono',monospace"; c.style.fontSize = "0.62rem"; c.style.textAlign = "center"; return c; }
    g.appendChild(cell("", "")); d.params.forEach(function (p) { var c = cell(p, ""); c.style.color = "#e7c98a"; c.style.textTransform = "uppercase"; c.style.letterSpacing = ".08em"; g.appendChild(c); });
    var read = el("div", "iact-readout"); read.style.marginTop = "0.8rem";
    d.features.forEach(function (f, i) {
      var rl = cell(f, ""); rl.style.color = "#f3ecd6"; rl.style.textAlign = "right"; rl.style.fontFamily = "'DM Sans',sans-serif"; rl.style.fontSize = "0.78rem"; g.appendChild(rl);
      d.params.forEach(function (p, j) {
        var v = d.matrix[i][j], t = Math.max(0, Math.min(1, v));
        var bg = "rgb(" + Math.round(lerp(13, 200, t)) + "," + Math.round(lerp(89, 160, t)) + "," + Math.round(lerp(99, 92, t)) + ")";
        var c = cell(v.toFixed(2), ""); c.style.background = bg; c.style.color = t > 0.55 ? "#052e36" : "#f3ecd6"; c.style.borderRadius = "2px"; c.style.cursor = "pointer";
        if (d.gold_bar && v >= d.gold_bar) { c.style.outline = "1.5px solid #f3ecd6"; }
        c.onclick = function () { read.innerHTML = "<b>" + f + "</b> carries <b style='color:#e7c98a'>" + v.toFixed(3) + "</b> importance for <b>" + p + "</b>" + (d.gold_bar && v >= d.gold_bar ? " (above the reliability bar)" : ""); };
        g.appendChild(c);
      });
    });
    mount.appendChild(read);
  }

  /* ---------- H. IDENTIFIABILITY EXPLORER (Theme 04) ---------- */
  function idbars(mount, d) {
    header(mount, "Which knobs can we recover?", "leave-one-out recovery R-squared per parameter");
    var TIER = { identifiable: C.green, weak: C.gold, "non-identifiable": C.muted };
    var vkeys = Object.keys(d.variants), cur = vkeys.indexOf("tau") >= 0 ? "tau" : vkeys[0];
    var seg = el("div", "iact-seg"); mount.appendChild(seg);
    var leg = el("div", "iact-readout"); leg.innerHTML = "<span style='color:" + C.green + "'>&#9632; identifiable</span> &nbsp; <span style='color:" + C.gold + "'>&#9632; weakly</span> &nbsp; <span style='color:" + C.muted + "'>&#9632; non-identifiable</span>"; mount.appendChild(leg);
    var cwrap = el("div"); mount.appendChild(cwrap);
    var det = el("div", "iact-readout"); mount.appendChild(det);
    function segBtns() { seg.innerHTML = ""; vkeys.forEach(function (k) { var b = chip(d.variants[k].label || k, k === cur); b.onclick = function () { cur = k; render(); }; seg.appendChild(b); }); }
    var canvas, geom = [];
    function render() {
      segBtns(); cwrap.innerHTML = ""; var bars = d.variants[cur].bars; canvas = mkCanvas(cwrap, 34 * bars.length + 30);
      var draw = function () {
        var x = ctxOf(canvas), W = canvas.clientWidth, H = canvas.clientHeight / DPR, padL = 110, padR = 54, bh = (H - 16) / bars.length; geom = [];
        x.clearRect(0, 0, W, H);
        bars.forEach(function (b, i) {
          var y = 8 + i * bh, w = (W - padL - padR) * Math.max(0, Math.min(1, b.r2)); geom.push({ y: y, bh: bh, b: b });
          x.fillStyle = TIER[b.tier] || C.gold; x.fillRect(padL, y + bh * 0.2, w, bh * 0.5);
          x.fillStyle = C.cream; x.font = "12px 'DM Sans'"; x.textAlign = "right"; x.fillText(b.param.replace(/_/g, " "), padL - 8, y + bh * 0.5);
          x.textAlign = "left"; x.fillStyle = C.goldL; x.fillText("R² " + b.r2.toFixed(2), padL + w + 6, y + bh * 0.5);
        });
        var thr = d.meta && d.meta.identifiable_threshold != null ? d.meta.identifiable_threshold : 0.75;
        var tx = padL + (W - padL - padR) * thr;
        x.setLineDash([5, 4]); x.strokeStyle = C.green; x.lineWidth = 1.5; x.beginPath(); x.moveTo(tx, 14); x.lineTo(tx, H - 4); x.stroke(); x.setLineDash([]);
        x.fillStyle = C.green; x.font = "10px 'JetBrains Mono'"; x.textAlign = "center"; x.fillText("identifiable " + thr, tx, 9);
        canvas._draw = draw;
      }; draw();
      canvas.onclick = function (e) { var r = canvas.getBoundingClientRect(), my = e.clientY - r.top, hit = geom.filter(function (gg) { return my >= gg.y && my <= gg.y + gg.bh; })[0]; if (hit) { var b = hit.b; det.innerHTML = "<b>" + b.param.replace(/_/g, " ") + "</b>: tier <b style='color:" + (TIER[b.tier]) + "'>" + b.tier + "</b>, R² " + b.r2.toFixed(3) + ", Pearson " + b.pearson.toFixed(3) + ", n " + b.n + (b.mean_abs_err != null ? ", MAE " + b.mean_abs_err.toFixed(3) : ""); } };
    }
    render();
  }

  /* ---------- I. DRUG PANEL FOREST (Theme 05) ---------- */
  function forest(mount, d) {
    header(mount, "Drug panel: inferred cell-cell adhesion shift", "each drug's delta J_cc with bootstrap interval; click for the wells behind it");
    var SIG = { sig: C.green, borderline: C.gold, ns: C.muted };
    var rows = d.rows.slice().sort(function (a, b) { return (a.order - b.order) || (a.est - b.est); });
    var leg = el("div", "iact-readout"); leg.innerHTML = "<span style='color:" + C.green + "'>&#9632; significant</span> &nbsp; <span style='color:" + C.gold + "'>&#9632; borderline</span> &nbsp; <span style='color:" + C.muted + "'>&#9632; not significant</span> &nbsp; dashed line = no change (0)"; mount.appendChild(leg);
    var grid = el("div", "iact-2col"); mount.appendChild(grid);
    var cwrap = el("div"); grid.appendChild(cwrap);
    var card = el("div", "iact-card"); grid.appendChild(card); card.innerHTML = "<div class='iact-hint'>Click a drug row.</div>";
    var lo = Math.min.apply(null, rows.map(function (r) { return r.lo; })), hi = Math.max.apply(null, rows.map(function (r) { return r.hi; }));
    var pad = (hi - lo) * 0.06; var xr = [lo - pad, hi + pad];
    var H = 22 * rows.length + 36; var canvas = mkCanvas(cwrap, H); var geom = [];
    function draw() {
      var x = ctxOf(canvas), W = canvas.clientWidth, padL = 132, padR = 40; geom = [];
      var px = function (v) { return lerp(padL, W - padR, (v - xr[0]) / (xr[1] - xr[0])); };
      x.clearRect(0, 0, W, H);
      var zx = px(0); x.setLineDash([4, 4]); x.strokeStyle = C.muted; x.lineWidth = 1; x.beginPath(); x.moveTo(zx, 18); x.lineTo(zx, H - 8); x.stroke(); x.setLineDash([]);
      rows.forEach(function (r, i) {
        var y = 24 + i * 22, col = SIG[r.sig] || C.gold; geom.push({ y: y, r: r });
        x.strokeStyle = col; x.lineWidth = 1.5; x.beginPath(); x.moveTo(px(r.lo), y); x.lineTo(px(r.hi), y); x.stroke();
        var rad = Math.max(3, Math.min(7, 2 + Math.sqrt(r.n))); x.beginPath(); x.arc(px(r.est), y, rad, 0, 7); x.fillStyle = col; x.fill();
        x.fillStyle = C.cream; x.font = "11px 'DM Sans'"; x.textAlign = "right"; x.fillText(r.label, padL - 8, y + 3);
      });
      x.fillStyle = C.muted; x.font = "11px 'DM Sans'"; x.textAlign = "center"; x.fillText(d.meta.x_label, (padL + W - padR) / 2, 12);
      canvas._draw = draw;
    }
    function show(r) {
      var wells = (d.details && d.details[r.label]) || [];
      var h = "<div class='iact-cardh'>" + r.label + " <span class='iact-badge' style='background:" + (SIG[r.sig]) + ";color:var(--teal-1)'>" + r.sig + "</span></div>";
      var kv = "<div class='iact-kv'><div class='iact-kvg'>" + r.cls + "</div><div><span>delta J_cc</span><b>" + fmt(r.est, 2) + "</b></div><div><span>interval</span><b>[" + fmt(r.lo, 2) + ", " + fmt(r.hi, 2) + "]</b></div><div><span>wells</span><b>" + r.n + "</b></div></div>";
      if (wells.length) { kv += "<div class='iact-kv'><div class='iact-kvg'>wells (" + wells.length + ")</div>"; wells.slice(0, 8).forEach(function (w) { kv += "<div><span>P" + w.patient + " " + (w.stim || "") + "</span><b>" + fmt(w.delta, 2) + "</b></div>"; }); if (wells.length > 8) kv += "<div><span>...</span><b>+" + (wells.length - 8) + "</b></div>"; kv += "</div>"; }
      card.innerHTML = h + kv;
    }
    canvas.addEventListener("click", function (e) { var r = canvas.getBoundingClientRect(), my = e.clientY - r.top, hit = geom.filter(function (g) { return Math.abs(g.y - my) <= 11; })[0]; if (hit) { show(hit.r); } });
    draw();
  }

  var WIDGETS = { morph: morphStudio, morphospace: morphospace, coverage: coverage, surrogate: surrogate,
    qcthreshold: qcthreshold, modelscatter: modelscatter, heatmap: heatmap, idbars: idbars, forest: forest };
  function boot() {
    var mounts = document.querySelectorAll(".iact[data-widget]");
    Array.prototype.forEach.call(mounts, function (m) {
      var w = WIDGETS[m.getAttribute("data-widget")], src = m.getAttribute("data-json");
      if (!w || !src) return;
      fetch(src).then(function (r) { return r.json(); }).then(function (d) { try { w(m, d); } catch (e) { m.innerHTML = "<div class='iact-hint'>interactive failed to load</div>"; console.error(e); } })
        .catch(function (e) { m.innerHTML = "<div class='iact-hint'>data unavailable</div>"; console.error(e); });
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
