// Extrae de biblioteca-movimiento.html el motor base, las recetas y el prompt para IA,
// en archivos que la búsqueda indexa y que un modelo local puede leer sin abrir el HTML.
//   node extraer_recetas.mjs <biblioteca-movimiento.html> <carpeta destino>
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const [html, destino] = process.argv.slice(2);
const t = fs.readFileSync(html, 'utf8');
const bloque = id => t.match(new RegExp(`<script id="${id}">([\\s\\S]*?)</script>`))[1];
const entidades = s => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');

const motor = bloque('engine');
const ctx = vm.createContext({ Math, console });
vm.runInContext(`${motor}\n${bloque('recipes')}\n;globalThis.__D = DEMOS;`, ctx);
const VER = vm.runInContext(`(${bloque('app').match(/const VER = (\{[^\n]*\});/)[1]})`, ctx);

const recetas = ctx.__D.map(d => ({
  id: d.id,
  nombre: d.name,
  categoria: d.cat,
  fuente: d.src,
  verificacion: VER[d.ver][0],
  nota_verificacion: VER[d.ver][2],
  bucle_s: +d.L.toFixed(3),
  que_se_mueve: d.que,
  pasos: d.pasos,
  parametros: d.params,
  codigo: 'draw' + d.draw.toString().replace(/^draw/, ''),
}));

// El HTML trae un <canvas> literal dentro del <pre> (el navegador lo vuelve un lienzo vacío): se rescata como texto.
const prompt = entidades(t.match(/<pre id="prompt-ia">([\s\S]*?)<\/pre>/)[1].replace(/<canvas>(<\/canvas>)?/g, '&lt;canvas&gt;').replace(/<[^>]+>/g, ''));
fs.mkdirSync(destino, { recursive: true });
fs.writeFileSync(path.join(destino, 'motor.js'), motor.trim() + '\n');
fs.writeFileSync(path.join(destino, 'recetas.json'), JSON.stringify(recetas, null, 2) + '\n');
fs.writeFileSync(path.join(destino, 'prompt-animador.md'),
  '# Prompt de sistema: animador de motion graphics (Canvas 2D)\n\n' +
  'Extraído de `biblioteca-movimiento.html`. Úsalo junto con `motor.js` y las recetas de `recetas.json`.\n\n' +
  '```text\n' + prompt.trim() + '\n```\n');
console.log(`${recetas.length} recetas, motor de ${motor.split('\n').length} líneas, prompt de ${prompt.length} caracteres`);
