// Level Editor Logic

const CELL_SIZE = 40;
let currentTool = "grass";
let level = {
  blocks: [],
  fires: [],
  objects: [],
};

// DOM Elements
const gridContainer = document.getElementById("grid-container");
const grid = document.getElementById("grid");
const grassTool = document.getElementById("grass-tool");
const fireTool = document.getElementById("fire-tool");
const fanTool = document.getElementById("fan-tool");
const sawTool = document.getElementById("saw-tool");
const fallingPlatformTool = document.getElementById("falling-platform-tool");
const finishTool = document.getElementById("finish-tool");
const eraseTool = document.getElementById("erase-tool");
const downloadBtn = document.getElementById("download-btn");
const clearBtn = document.getElementById("clear-btn");
const coordinates = document.getElementById("coordinates");
const levelFileInput = document.getElementById("level-file");

// Track visible cells
let visibleCells = new Map(); // Map of "x,y" to cell element

// Initialize grid
function initGrid() {
  // Create initial cells
  const initialSize = 50; // 50x50 grid to start
  for (let y = 0; y < initialSize; y++) {
    for (let x = 0; x < initialSize; x++) {
      createCell(x, y);
    }
  }

  // Add scroll event listener
  gridContainer.addEventListener("scroll", handleScroll);

  // Add mouse move event for coordinates
  gridContainer.addEventListener("mousemove", handleMouseMove);
}

function createCell(x, y) {
  const key = `${x},${y}`;
  if (visibleCells.has(key)) return;

  const cell = document.createElement("div");
  cell.className = "grid-cell";
  // Position from bottom-left
  cell.style.left = `${x * CELL_SIZE}px`;
  cell.style.bottom = `${y * CELL_SIZE}px`;
  cell.dataset.x = x;
  cell.dataset.y = y;
  cell.addEventListener("click", () => handleCellClick(x, y));

  // Check if there's a block, fire, or object at this position
  const block = level.blocks.find((b) => b.x === x && b.y === y);
  const fire = level.fires.find((f) => f.x === x && f.y === y);
  const object = level.objects.find((o) => o.x === x && o.y === y);

  if (block) cell.classList.add("grass");
  if (fire) cell.classList.add("fire");
  if (object) cell.classList.add(object.type.toLowerCase());

  grid.appendChild(cell);
  visibleCells.set(key, cell);
}

function handleScroll() {
  const containerWidth = gridContainer.clientWidth;
  const containerHeight = gridContainer.clientHeight;
  const scrollLeft = gridContainer.scrollLeft;
  const scrollTop = gridContainer.scrollTop;

  // Calculate visible range from bottom-left
  const startX = Math.floor(scrollLeft / CELL_SIZE);
  const startY = Math.floor(scrollTop / CELL_SIZE);
  const endX = Math.ceil((scrollLeft + containerWidth) / CELL_SIZE);
  const endY = Math.ceil((scrollTop + containerHeight) / CELL_SIZE);

  // Create cells for visible area
  for (let y = startY; y < endY; y++) {
    for (let x = startX; x < endX; x++) {
      createCell(x, y);
    }
  }
}

function handleMouseMove(e) {
  const rect = gridContainer.getBoundingClientRect();
  const x = Math.floor(
    (e.clientX - rect.left + gridContainer.scrollLeft) / CELL_SIZE
  );
  const y = Math.floor(
    (rect.bottom - e.clientY + gridContainer.scrollTop) / CELL_SIZE
  );
  coordinates.textContent = `X: ${x}, Y: ${y}`;
}

// Tool selection
function setActiveTool(tool) {
  currentTool = tool;
  [
    grassTool,
    fireTool,
    fanTool,
    sawTool,
    fallingPlatformTool,
    finishTool,
    eraseTool,
  ].forEach((btn) => btn.classList.remove("active"));
  document.getElementById(`${tool}-tool`).classList.add("active");
}

grassTool.addEventListener("click", () => setActiveTool("grass"));
fireTool.addEventListener("click", () => setActiveTool("fire"));
fanTool.addEventListener("click", () => setActiveTool("fan"));
sawTool.addEventListener("click", () => setActiveTool("saw"));
fallingPlatformTool.addEventListener("click", () =>
  setActiveTool("falling-platform")
);
finishTool.addEventListener("click", () => setActiveTool("finish"));
eraseTool.addEventListener("click", () => setActiveTool("erase"));

// Handle cell clicks
function handleCellClick(x, y) {
  const cell = visibleCells.get(`${x},${y}`);
  if (!cell) return;

  // Remove existing elements at this position
  level.blocks = level.blocks.filter((b) => !(b.x === x && b.y === y));
  level.fires = level.fires.filter((f) => !(f.x === x && f.y === y));
  level.objects = level.objects.filter((o) => !(o.x === x && o.y === y));
  cell.classList.remove(
    "grass",
    "fire",
    "fan",
    "saw",
    "fallingplatform",
    "finish"
  );

  // Add new element if not erasing
  if (currentTool !== "erase") {
    if (currentTool === "grass") {
      level.blocks.push({ type: "grass", x, y });
      cell.classList.add("grass");
    } else if (currentTool === "fire") {
      level.fires.push({ x, y });
      cell.classList.add("fire");
    } else if (currentTool === "fan") {
      level.objects.push({ type: "Fan", x, y });
      cell.classList.add("fan");
    } else if (currentTool === "saw") {
      level.objects.push({ type: "Saw", x, y });
      cell.classList.add("saw");
    } else if (currentTool === "falling-platform") {
      level.objects.push({ type: "FallingPlatform", x, y });
      cell.classList.add("fallingplatform");
    } else if (currentTool === "finish") {
      level.objects.push({ type: "Finish", x, y });
      cell.classList.add("finish");
    }
  }
}

// Download level
function downloadLevel() {
  const blob = new Blob([JSON.stringify(level, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "level.json";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// Clear level
function clearLevel() {
  if (!confirm("Are you sure you want to clear the level?")) return;
  level = { blocks: [], fires: [], objects: [] };
  visibleCells.forEach((cell) => {
    cell.classList.remove(
      "grass",
      "fire",
      "fan",
      "saw",
      "fallingplatform",
      "finish"
    );
  });
}

// Load level from JSON
function loadLevel(json) {
  level = json;
  // Ensure backwards compatibility
  if (!level.objects) level.objects = [];

  visibleCells.forEach((cell) => {
    cell.classList.remove(
      "grass",
      "fire",
      "fan",
      "saw",
      "fallingplatform",
      "finish"
    );
  });

  level.blocks.forEach((block) => {
    const cell = visibleCells.get(`${block.x},${block.y}`);
    if (cell) cell.classList.add("grass");
  });

  if (level.fires) {
    level.fires.forEach((fire) => {
      const cell = visibleCells.get(`${fire.x},${fire.y}`);
      if (cell) cell.classList.add("fire");
    });
  }

  if (level.objects) {
    level.objects.forEach((object) => {
      const cell = visibleCells.get(`${object.x},${object.y}`);
      if (cell) cell.classList.add(object.type.toLowerCase());
    });
  }
}

// Handle file input
levelFileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (event) => {
    try {
      const json = JSON.parse(event.target.result);
      loadLevel(json);
    } catch (error) {
      alert("Error loading level file: " + error.message);
    }
  };
  reader.readAsText(file);
});

// Event listeners
downloadBtn.addEventListener("click", downloadLevel);
clearBtn.addEventListener("click", clearLevel);

// Initialize
initGrid();
