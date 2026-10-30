const expressionInput = document.querySelector("#expression");
const calculateButton = document.querySelector("#calculate-button");
const nextButton = document.querySelector("#next-button");
const playButton = document.querySelector("#play-button");
const resetButton = document.querySelector("#reset-button");
const treeContainer = document.querySelector("#tree-container");
const postorderOutput = document.querySelector("#postorder-output");
const resultOutput = document.querySelector("#result-output");
const stepDescription = document.querySelector("#step-description");
const stepsOutput = document.querySelector("#steps-output");
const errorMessage = document.querySelector("#error-message");

let calculation = null;
let currentStep = -1;
let playTimer = null;

function escapeText(value) {
    return String(value);
}

function collectLayout(node, depth, state, positions, edges) {
    if (!node) {
        return null;
    }

    const leftPosition = collectLayout(node.left, depth + 1, state, positions, edges);
    const position = { node, x: state.nextX, y: depth };
    state.nextX += 1;
    positions.push(position);
    const rightPosition = collectLayout(node.right, depth + 1, state, positions, edges);

    if (leftPosition) {
        edges.push({ parent: position, child: leftPosition });
    }
    if (rightPosition) {
        edges.push({ parent: position, child: rightPosition });
    }

    return position;
}

function renderTree(root, activeNodeId = null, errorNodeId = null) {
    if (!root) {
        treeContainer.innerHTML = '<p class="empty-state">Construye una expresión para mostrar su árbol.</p>';
        return;
    }

    const positions = [];
    const edges = [];
    collectLayout(root, 0, { nextX: 0 }, positions, edges);

    const horizontalSpacing = 100;
    const verticalSpacing = 90;
    const padding = 60;
    const maxDepth = Math.max(...positions.map((item) => item.y));
    const width = Math.max(620, (positions.length + 1) * horizontalSpacing + padding * 2);
    const height = Math.max(380, (maxDepth + 1) * verticalSpacing + padding * 2);
    const maxX = Math.max(...positions.map((item) => item.x));
    const xOffset = (width - (maxX * horizontalSpacing + padding * 2)) / 2 + padding;

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("class", "tree-svg");
    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);

    const coordinates = new Map();
    positions.forEach((item) => {
        coordinates.set(item.node.id, {
            x: item.x * horizontalSpacing + xOffset,
            y: item.y * verticalSpacing + padding,
        });
    });

    edges.forEach(({ parent, child }) => {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        const parentPoint = coordinates.get(parent.node.id);
        const childPoint = coordinates.get(child.node.id);
        line.setAttribute("class", "tree-edge");
        line.setAttribute("x1", parentPoint.x);
        line.setAttribute("y1", parentPoint.y);
        line.setAttribute("x2", childPoint.x);
        line.setAttribute("y2", childPoint.y);
        svg.appendChild(line);
    });

    positions.forEach((item) => {
        const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        const point = coordinates.get(item.node.id);
        const nodeClass = item.node.type === "operator" ? "operator" : "number";

        group.setAttribute("class", `tree-node ${nodeClass}${item.node.id === activeNodeId ? " active" : ""}${item.node.id === errorNodeId ? " error" : ""}`);
        rect.setAttribute("x", point.x - 31);
        rect.setAttribute("y", point.y - 24);
        rect.setAttribute("width", 62);
        rect.setAttribute("height", 48);
        rect.setAttribute("rx", 12);
        text.setAttribute("x", point.x);
        text.setAttribute("y", point.y + 1);
        text.textContent = escapeText(item.node.value);
        group.appendChild(rect);
        group.appendChild(text);
        svg.appendChild(group);
    });

    treeContainer.replaceChildren(svg);
}

function describeStep(step) {
    if (!step) {
        return "Todavía no se ha iniciado el recorrido.";
    }
    if (step.action === "visit") {
        return `Se visita el nodo ${step.value}.`;
    }
    if (step.action === "calculate") {
        return `${step.left} ${step.value} ${step.right} = ${step.result}`;
    }
    return step.message;
}

function renderSteps() {
    if (!calculation || calculation.steps.length === 0) {
        stepsOutput.innerHTML = '<li class="empty-state">Los pasos aparecerán después de construir el árbol.</li>';
        return;
    }

    stepsOutput.replaceChildren(...calculation.steps.map((step, index) => {
        const item = document.createElement("li");
        item.textContent = describeStep(step);
        if (index === currentStep) {
            item.classList.add("current");
        }
        if (step.action === "error") {
            item.classList.add("error-step");
        }
        return item;
    }));
}

function renderCurrentStep() {
    if (!calculation) {
        return;
    }

    const step = calculation.steps[currentStep];
    const errorNodeId = calculation.errorNodeId || (step && step.action === "error" ? step.node_id : null);
    renderTree(calculation.tree, step ? step.node_id : null, errorNodeId);
    stepDescription.textContent = describeStep(step);
    renderSteps();

    nextButton.disabled = currentStep >= calculation.steps.length - 1;
    playButton.disabled = currentStep >= calculation.steps.length - 1;
    playButton.textContent = playTimer ? "Pausar" : "Reproducir";
}

function stopPlaying() {
    if (playTimer) {
        clearInterval(playTimer);
        playTimer = null;
    }
    playButton.textContent = "Reproducir";
}

function nextStep() {
    if (!calculation || currentStep >= calculation.steps.length - 1) {
        stopPlaying();
        return;
    }
    currentStep += 1;
    renderCurrentStep();
}

function togglePlaying() {
    if (!calculation) {
        return;
    }
    if (playTimer) {
        stopPlaying();
        return;
    }
    if (currentStep >= calculation.steps.length - 1) {
        currentStep = -1;
    }
    playTimer = setInterval(nextStep, 900);
    nextStep();
    renderCurrentStep();
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.hidden = false;
}

function clearError() {
    errorMessage.textContent = "";
    errorMessage.hidden = true;
}

async function calculate() {
    stopPlaying();
    clearError();
    calculateButton.disabled = true;
    calculateButton.textContent = "Construyendo...";

    try {
        const response = await fetch("/api/calculate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ expression: expressionInput.value }),
        });
        const payload = await response.json();
        calculation = {
            tree: payload.tree || null,
            steps: payload.steps || [],
            errorNodeId: payload.error_node_id || null,
        };
        currentStep = -1;
        postorderOutput.textContent = (payload.postorder || payload.postfix || []).join("  ") || "—";
        resultOutput.textContent = payload.ok ? payload.result : "Error";
        if (!payload.ok) {
            showError(payload.error || "No se pudo procesar la expresión.");
        }
        nextButton.disabled = !calculation.steps.length;
        playButton.disabled = !calculation.steps.length;
        renderTree(calculation.tree, null, calculation.errorNodeId);
        renderSteps();
        renderCurrentStep();
    } catch (error) {
        calculation = null;
        renderTree(null);
        showError("No fue posible comunicarse con el servidor.");
    } finally {
        calculateButton.disabled = false;
        calculateButton.textContent = "Construir árbol";
    }
}

function reset() {
    stopPlaying();
    calculation = null;
    currentStep = -1;
    clearError();
    renderTree(null);
    postorderOutput.textContent = "—";
    resultOutput.textContent = "—";
    stepDescription.textContent = "Todavía no se ha iniciado el recorrido.";
    renderSteps();
    nextButton.disabled = true;
    playButton.disabled = true;
}

calculateButton.addEventListener("click", calculate);
nextButton.addEventListener("click", nextStep);
playButton.addEventListener("click", togglePlaying);
resetButton.addEventListener("click", reset);
expressionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        calculate();
    }
});
