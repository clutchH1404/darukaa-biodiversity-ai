import React, { useEffect, useRef } from "react";

export const AtmosphericShader: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const gl = canvas.getContext("webgl");
    if (!gl) return;

    let animationFrameId: number;

    const vsSource = `
      attribute vec2 position;
      void main() {
        gl_Position = vec4(position, 0.0, 1.0);
      }
    `;

    const fsSource = `
      precision mediump float;
      uniform vec2 u_resolution;
      uniform float u_time;
      uniform vec2 u_mouse;

      // 2D Simplex-like Noise
      vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
      vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
      vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

      float snoise(vec2 v) {
        const vec4 C = vec4(0.211324865405187, 0.366025403784439, -0.577350269189626, 0.024390243902439);
        vec2 i  = floor(v + dot(v, C.yy));
        vec2 x0 = v -   i + dot(i, C.xx);
        vec2 i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
        vec4 x12 = x0.xyxy + C.xxzz;
        x12.xy -= i1;
        i = mod289(i);
        vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0));
        vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
        m = m*m;
        m = m*m;
        vec3 x = 2.0 * fract(p * C.www) - 1.0;
        vec3 h = abs(x) - 0.5;
        vec3 ox = floor(x + 0.5);
        vec3 a0 = x - ox;
        m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
        vec3 g;
        g.x  = a0.x  * x0.x  + h.x  * x0.y;
        g.yz = a0.yz * x12.xz + h.yz * x12.yw;
        return 130.0 * dot(m, g);
      }

      void main() {
        vec2 st = gl_FragCoord.xy / u_resolution.xy;
        st.x *= u_resolution.x / u_resolution.y;

        vec2 mouse = u_mouse / u_resolution.xy;
        float distToMouse = length(st - mouse);

        // Multi-octave planetary atmospheric flow
        vec2 q = vec2(0.0);
        q.x = snoise(st + vec2(0.0, 0.04 * u_time));
        q.y = snoise(st + vec2(0.04 * u_time, 0.0));

        vec2 r = vec2(0.0);
        r.x = snoise(st + 1.0 * q + vec2(1.7, 9.2) + 0.08 * u_time);
        r.y = snoise(st + 1.0 * q + vec2(8.3, 2.8) + 0.08 * u_time);

        float f = snoise(st + r);

        // BIOSPHÈRE COLOR PALETTE (Stitch: Deep Navy, Bio-Emerald, Cyan, Warm Amber)
        vec3 colorBg = vec3(0.067, 0.075, 0.098);    // #111319 Deep cosmic navy
        vec3 colorBio = vec3(0.306, 0.871, 0.639);   // #4edea3 Vibrant Emerald
        vec3 colorCyan = vec3(0.298, 0.843, 0.965);  // #4cd7f6 Biosphere Cyan
        vec3 colorWarn = vec3(1.000, 0.725, 0.373);  // #ffb95f Amber

        vec3 color = mix(colorBg, colorCyan, clamp(length(q), 0.0, 1.0));
        color = mix(color, colorBio, clamp(length(r.x), 0.0, 1.0));
        color = mix(color, colorWarn, clamp(pow(f, 3.0), 0.0, 0.15));

        // Vignette
        vec2 uv = gl_FragCoord.xy / u_resolution.xy;
        float vignette = uv.x * uv.y * (1.0 - uv.x) * (1.0 - uv.y);
        vignette = clamp(pow(16.0 * vignette, 0.35), 0.0, 1.0);

        gl_FragColor = vec4(color * vignette, 0.75);
      }
    `;

    function createShader(type: number, source: string) {
      if (!gl) return null;
      const shader = gl.createShader(type);
      if (!shader) return null;
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        gl.deleteShader(shader);
        return null;
      }
      return shader;
    }

    const vs = createShader(gl.VERTEX_SHADER, vsSource);
    const fs = createShader(gl.FRAGMENT_SHADER, fsSource);
    if (!vs || !fs) return;

    const program = gl.createProgram();
    if (!program) return;
    gl.attachShader(program, vs);
    gl.attachShader(program, fs);
    gl.linkProgram(program);

    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
      return;
    }

    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([
        -1.0, -1.0,
         1.0, -1.0,
        -1.0,  1.0,
        -1.0,  1.0,
         1.0, -1.0,
         1.0,  1.0
      ]),
      gl.STATIC_DRAW
    );

    const posAttr = gl.getAttribLocation(program, "position");
    gl.enableVertexAttribArray(posAttr);
    gl.vertexAttribPointer(posAttr, 2, gl.FLOAT, false, 0, 0);

    const resLoc = gl.getUniformLocation(program, "u_resolution");
    const timeLoc = gl.getUniformLocation(program, "u_time");
    const mouseLoc = gl.getUniformLocation(program, "u_mouse");

    let mouseX = 0;
    let mouseY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = window.innerHeight - e.clientY;
    };

    window.addEventListener("mousemove", handleMouseMove);

    const resize = () => {
      if (!canvas) return;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      gl.viewport(0, 0, canvas.width, canvas.height);
    };

    window.addEventListener("resize", resize);
    resize();

    const startTime = performance.now();

    const render = (time: number) => {
      const elapsed = (time - startTime) * 0.001;
      gl.useProgram(program);
      gl.uniform2f(resLoc, canvas.width, canvas.height);
      gl.uniform1f(timeLoc, elapsed);
      gl.uniform2f(mouseLoc, mouseX, mouseY);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      animationFrameId = requestAnimationFrame(render);
    };

    animationFrameId = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      id="bg-canvas"
      className="fixed inset-0 pointer-events-none z-0 opacity-40 transition-opacity duration-1000"
    />
  );
};
