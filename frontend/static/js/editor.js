# frontend/static/js/editor.js
class BlockEditor {
    constructor(container) {
        this.container = container;
        this.blocks = [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.container.addEventListener('keydown', this.handleKeydown.bind(this));
        this.container.addEventListener('paste', this.handlePaste.bind(this));
        document.addEventListener('click', this.handleClickOutside.bind(this));
    }

    createBlock(type = 'paragraph', content = '') {
        const block = document.createElement('div');
        block.className = 'notion-block';
        block.setAttribute('data-type', type);

        switch (type) {
            case 'heading_1':
                block.innerHTML = `<h1 class="notion-h1" contenteditable="true">${content}</h1>`;
                break;
            case 'heading_2':
                block.innerHTML = `<h2 class="notion-h2" contenteditable="true">${content}</h2>`;
                break;
            case 'heading_3':
                block.innerHTML = `<h3 class="notion-h3" contenteditable="true">${content}</h3>`;
                break;
            case 'todo':
                block.innerHTML = `
                    <div class="flex items-start gap-2">
                        <input type="checkbox" class="mt-1">
                        <div contenteditable="true" class="flex-1">${content}</div>
                    </div>`;
                break;
            case 'bullet_list':
                block.innerHTML = `<div class="flex items-start gap-2">
                    <span class="mt-1">•</span>
                    <div contenteditable="true" class="flex-1">${content}</div>
                </div>`;
                break;
            case 'numbered_list':
                block.innerHTML = `<div class="flex items-start gap-2">
                    <span class="mt-1">${this.blocks.length + 1}.</span>
                    <div contenteditable="true" class="flex-1">${content}</div>
                </div>`;
                break;
            case 'code':
                block.innerHTML = `<pre class="notion-code"><code contenteditable="true">${content}</code></pre>`;
                break;
            default:
                block.innerHTML = `<div contenteditable="true" class="notion-text">${content}</div>`;
        }

        return block;
    }

    showBlockMenu(position) {
        const menu = document.createElement('div');
        menu.className = 'notion-block-menu absolute bg-white shadow-lg rounded-lg p-2 z-50';
        menu.style.left = `${position.x}px`;
        menu.style.top = `${position.y}px`;

        const options = [
            { type: 'heading_1', label: 'Heading 1' },
            { type: 'heading_2', label: 'Heading 2' },
            { type: 'heading_3', label: 'Heading 3' },
            { type: 'paragraph', label: 'Text' },
            { type: 'todo', label: 'To-do' },
            { type: 'bullet_list', label: 'Bullet List' },
            { type: 'numbered_list', label: 'Numbered List' },
            { type: 'code', label: 'Code' }
        ];

        options.forEach(option => {
            const button = document.createElement('button');
            button.className = 'block w-full text-left px-4 py-2 hover:bg-gray-100 rounded';
            button.textContent = option.label;
            button.onclick = () => this.convertBlock(this.currentBlock, option.type);
            menu.appendChild(button);
        });

        document.body.appendChild(menu);
        this.blockMenu = menu;
    }

    convertBlock(block, type) {
        const content = this.getBlockContent(block);
        const newBlock = this.createBlock(type, content);
        block.parentNode.replaceChild(newBlock, block);
        this.hideBlockMenu();
    }

    getBlockContent(block) {
        const contentElement = block.querySelector('[contenteditable="true"]');
        return contentElement ? contentElement.textContent : '';
    }

    hideBlockMenu() {
        if (this.blockMenu) {
            this.blockMenu.remove();
            this.blockMenu = null;
        }
    }

    handleKeydown(event) {
        if (event.key === '/') {
            event.preventDefault();
            const selection = window.getSelection();
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();

            this.currentBlock = event.target.closest('.notion-block');
            this.showBlockMenu({
                x: rect.left,
                y: rect.bottom + window.scrollY
            });
        }
    }

    handlePaste(event) {
        event.preventDefault();
        const text = event.clipboardData.getData('text/plain');
        document.execCommand('insertText', false, text);
    }

    handleClickOutside(event) {
        if (this.blockMenu && !this.blockMenu.contains(event.target)) {
            this.hideBlockMenu();
        }
    }

    toJSON() {
        const blocks = Array.from(this.container.querySelectorAll('.notion-block'));
        return blocks.map(block => ({
            type: block.getAttribute('data-type'),
            content: this.getBlockContent(block)
        }));
    }

    fromJSON(data) {
        this.container.innerHTML = '';
        data.forEach(block => {
            const element = this.createBlock(block.type, block.content);
            this.container.appendChild(element);
        });
    }
}

// 드래그 앤 드롭 기능 확장
class DraggableBlocks {
    constructor(container) {
        this.container = container;
        this.initializeDragAndDrop();
    }

    initializeDragAndDrop() {
        this.container.addEventListener('dragstart', this.handleDragStart.bind(this));
        this.container.addEventListener('dragover', this.handleDragOver.bind(this));
        this.container.addEventListener('drop', this.handleDrop.bind(this));
    }

    handleDragStart(event) {
        const block = event.target.closest('.notion-block');
        if (!block) return;

        event.dataTransfer.setData('text/plain', block.getAttribute('data-type'));
        this.draggedElement = block;
    }

    handleDragOver(event) {
        event.preventDefault();
        const block = event.target.closest('.notion-block');
        if (!block || block === this.draggedElement) return;

        const rect = block.getBoundingClientRect();
        const midpoint = rect.top + rect.height / 2;

        if (event.clientY < midpoint) {
            block.style.borderTop = '2px solid #4299e1';
            block.style.borderBottom = '';
        } else {
            block.style.borderTop = '';
            block.style.borderBottom = '2px solid #4299e1';
        }
    }

    handleDrop(event) {
        event.preventDefault();
        const block = event.target.closest('.notion-block');
        if (!block || block === this.draggedElement) return;

        const rect = block.getBoundingClientRect();
        const midpoint = rect.top + rect.height / 2;

        if (event.clientY < midpoint) {
            block.parentNode.insertBefore(this.draggedElement, block);
        } else {
            block.parentNode.insertBefore(this.draggedElement, block.nextSibling);
        }

        // 드래그 표시 제거
        block.style.borderTop = '';
        block.style.borderBottom = '';
    }
}

// 초기화
document.addEventListener('DOMContentLoaded', () => {
    const editorContainer = document.querySelector('.notion-editor');
    if (editorContainer) {
        const editor = new BlockEditor(editorContainer);
        new DraggableBlocks(editorContainer);
    }
});