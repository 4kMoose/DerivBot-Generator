document.addEventListener('DOMContentLoaded', function() {
    // Initialize Sortable for components list
    new Sortable(document.getElementById('components-list'), {
        group: {
            name: 'shared',
            pull: 'clone',
            put: false
        },
        animation: 150,
        sort: false
    });

    // Initialize Sortable for strategy canvas
    new Sortable(document.getElementById('strategy-canvas'), {
        group: {
            name: 'shared',
            pull: true,
            put: true
        },
        animation: 150,
        onAdd: function(evt) {
            const item = evt.item;
            initializeComponent(item);
        }
    });

    // Initialize event listeners
    document.getElementById('saveBtn').addEventListener('click', saveStrategy);
    document.getElementById('deployBtn').addEventListener('click', deployStrategy);
});

function initializeComponent(component) {
    const type = component.getAttribute('data-type');
    let configHtml = '';

    switch(type) {
        case 'indicator':
            configHtml = createIndicatorConfig(component.textContent);
            break;
        case 'condition':
            configHtml = createConditionConfig();
            break;
        case 'action':
            configHtml = createActionConfig();
            break;
    }

    component.innerHTML += configHtml;
    component.classList.add('configured-component');
}

function createIndicatorConfig(indicatorType) {
    let config = '<div class="component-config mt-2 p-2 bg-gray-50 rounded">';
    
    switch(indicatorType.trim()) {
        case 'Moving Average':
            config += `
                <div class="mb-2">
                    <label class="block text-sm">Period</label>
                    <input type="number" class="w-full border rounded" value="14">
                </div>
                <div class="mb-2">
                    <label class="block text-sm">Type</label>
                    <select class="w-full border rounded">
                        <option value="sma">Simple</option>
                        <option value="ema">Exponential</option>
                    </select>
                </div>
            `;
            break;
        case 'RSI':
            config += `
                <div class="mb-2">
                    <label class="block text-sm">Period</label>
                    <input type="number" class="w-full border rounded" value="14">
                </div>
                <div class="mb-2">
                    <label class="block text-sm">Overbought</label>
                    <input type="number" class="w-full border rounded" value="70">
                </div>
                <div class="mb-2">
                    <label class="block text-sm">Oversold</label>
                    <input type="number" class="w-full border rounded" value="30">
                </div>
            `;
            break;
        case 'MACD':
            config += `
                <div class="mb-2">
                    <label class="block text-sm">Fast Period</label>
                    <input type="number" class="w-full border rounded" value="12">
                </div>
                <div class="mb-2">
                    <label class="block text-sm">Slow Period</label>
                    <input type="number" class="w-full border rounded" value="26">
                </div>
                <div class="mb-2">
                    <label class="block text-sm">Signal Period</label>
                    <input type="number" class="w-full border rounded" value="9">
                </div>
            `;
            break;
    }

    config += '</div>';
    return config;
}

function createConditionConfig() {
    return `
        <div class="component-config mt-2 p-2 bg-gray-50 rounded">
            <div class="mb-2">
                <label class="block text-sm">First Value</label>
                <select class="w-full border rounded">
                    <option value="price">Price</option>
                    <option value="ma">Moving Average</option>
                    <option value="rsi">RSI</option>
                </select>
            </div>
            <div class="mb-2">
                <label class="block text-sm">Condition</label>
                <select class="w-full border rounded">
                    <option value="crosses_above">Crosses Above</option>
                    <option value="crosses_below">Crosses Below</option>
                    <option value="greater_than">Greater Than</option>
                    <option value="less_than">Less Than</option>
                </select>
            </div>
            <div class="mb-2">
                <label class="block text-sm">Second Value</label>
                <select class="w-full border rounded">
                    <option value="price">Price</option>
                    <option value="ma">Moving Average</option>
                    <option value="rsi">RSI</option>
                </select>
            </div>
        </div>
    `;
}

function createActionConfig() {
    return `
        <div class="component-config mt-2 p-2 bg-gray-50 rounded">
            <div class="mb-2">
                <label class="block text-sm">Position Size</label>
                <input type="number" class="w-full border rounded" value="1">
            </div>
            <div class="mb-2">
                <label class="block text-sm">Stop Loss (pips)</label>
                <input type="number" class="w-full border rounded" value="50">
            </div>
            <div class="mb-2">
                <label class="block text-sm">Take Profit (pips)</label>
                <input type="number" class="w-full border rounded" value="100">
            </div>
        </div>
    `;
}

async function saveStrategy() {
    const strategy = buildStrategyObject();
    
    try {
        const response = await fetch('/api/strategy/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(strategy)
        });
        
        const result = await response.json();
        if (result.success) {
            alert('Strategy saved successfully!');
        } else {
            alert('Error saving strategy: ' + result.error);
        }
    } catch (error) {
        alert('Error saving strategy: ' + error.message);
    }
}

async function deployStrategy() {
    const strategy = buildStrategyObject();
    
    try {
        const response = await fetch('/api/strategy/deploy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(strategy)
        });
        
        const result = await response.json();
        if (result.success) {
            alert('Strategy deployed successfully!');
        } else {
            alert('Error deploying strategy: ' + result.error);
        }
    } catch (error) {
        alert('Error deploying strategy: ' + error.message);
    }
}

function buildStrategyObject() {
    const canvas = document.getElementById('strategy-canvas');
    const components = Array.from(canvas.children);
    
    return {
        name: 'My Strategy',
        components: components.map(component => ({
            type: component.getAttribute('data-type'),
            name: component.textContent.split('\n')[0].trim(),
            config: extractComponentConfig(component)
        })),
        properties: {
            riskTolerance: document.getElementById('riskTolerance').value,
            tradingSession: document.getElementById('tradingSession').value,
            assetClass: document.getElementById('assetClass').value
        }
    };
}

function extractComponentConfig(component) {
    const config = {};
    const inputs = component.querySelectorAll('input, select');
    
    inputs.forEach(input => {
        const label = input.previousElementSibling.textContent;
        config[label.toLowerCase()] = input.value;
    });
    
    return config;
}
