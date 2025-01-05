# frontend/static/js/main.js
// API 호출 함수들
const api = {
    async fetchPages() {
        const response = await fetch('/api/v1/pages');
        return await response.json();
    },

    async createPage(pageData) {
        const response = await fetch('/api/v1/pages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pageData),
        });
        return await response.json();
    },

    async updatePage(pageId, pageData) {
        const response = await fetch(`/api/v1/pages/${pageId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(pageData),
        });
        return await response.json();
    },

    async fetchDatabases() {
        const response = await fetch('/api/v1/databases');
        return await response.json();
    },

    async createDatabase(dbData) {
        const response = await fetch('/api/v1/databases', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dbData),
        });
        return await response.json();
    },
};

// 에디터 관련 기능
class NotionEditor {
    constructor(element) {
        this.element = element;
        this.content = {};
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.element.addEventListener('keydown', this.handleKeyDown.bind(this));
        this.element.addEventListener('input', this.handleInput.bind(this));
    }

    handleKeyDown(event) {
        if (event.key === '/') {
            this.showCommandPalette();
        }
    }

    handleInput(event) {
        this.saveContent();
    }

    showCommandPalette() {
        // 커맨드 팔레트 UI 표시
        const palette = document.createElement('div');
        palette.classList.add('notion-command-palette');
        // ... 커맨드 팔레트 구현
    }

    saveContent() {
        // 내용 저장 로직
        this.content = {
            blocks: this.parseContent()
        };
    }

    parseContent() {
        // 에디터 내용을 블록 단위로 파싱
        return [];
    }
}

// 데이터베이스 뷰 관련 기능
class NotionDatabase {
    constructor(element, data) {
        this.element = element;
        this.data = data;
        this.currentView = 'table';
    }

    render() {
        switch (this.currentView) {
            case 'table':
                this.renderTableView();
                break;
            case 'board':
                this.renderBoardView();
                break;
            case 'calendar':
                this.renderCalendarView();
                break;
            case 'gallery':
                this.renderGalleryView();
                break;
        }
    }

    renderTableView() {
        // 테이블 뷰 렌더링
    }

    renderBoardView() {
        // 보드 뷰 렌더링
    }

    renderCalendarView() {
        // 캘린더 뷰 렌더링
    }

    renderGalleryView() {
        // 갤러리 뷰 렌더링
    }

    changeView(viewType) {
        this.currentView = viewType;
        this.render();
    }
}

// 드래그 앤 드롭 기능
class DragAndDrop {
    constructor(element) {
        this.element = element;
        this.setupDragAndDrop();
    }

    setupDragAndDrop() {
        this.element.addEventListener('dragstart', this.handleDragStart.bind(this));
        this.element.addEventListener('dragover', this.handleDragOver.bind(this));
        this.element.addEventListener('drop', this.handleDrop.bind(this));
    }

    handleDragStart(event) {
        event.dataTransfer.setData('text/plain', event.target.id);
    }

    handleDragOver(event) {
        event.preventDefault();
    }

    handleDrop(event) {
        event.preventDefault();
        const id = event.dataTransfer.getData('text/plain');
        // 드롭 처리 로직
    }
}

// 페이지 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 에디터 초기화
    const editorElements = document.querySelectorAll('.notion-editor');
    editorElements.forEach(element => {
        new NotionEditor(element);
    });

    // 데이터베이스 초기화
    const dbElements = document.querySelectorAll('.notion-database');
    dbElements.forEach(element => {
        new NotionDatabase(element);
    });
});