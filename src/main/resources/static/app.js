// ═══════════════════════════════════════════════════════
//  CampiFi — app.js
//  Covers: homepage login, channel browser,
//          admin dashboard (network & admin management), and chat.
// ═══════════════════════════════════════════════════════

// ── Session storage helpers ──────────────────────────────────────────────────

function saveSession(token, displayName, email, role) {
    sessionStorage.setItem('campifi_token',   token);
    sessionStorage.setItem('campifi_name',    displayName);
    sessionStorage.setItem('campifi_email',   email);
    sessionStorage.setItem('campifi_role',    role);
}
function getSessionToken() { return sessionStorage.getItem('campifi_token'); }
function getSessionName()  { return sessionStorage.getItem('campifi_name');  }
function getSessionRole()  { return sessionStorage.getItem('campifi_role');  }
function getSessionEmail() { return sessionStorage.getItem('campifi_email'); }
function clearSession() {
    ['campifi_token','campifi_name','campifi_email','campifi_role']
        .forEach(k => sessionStorage.removeItem(k));
}

// ── Email → display name ─────────────────────────────────────────────────────

function parseEmailToName(email) {
    if (!email || !email.includes('@')) return (email || '').trim();
    let local = email.split('@')[0].toLowerCase();
    let parts = local.split(/[._\-]+/)
        .map(p => p.replace(/^\d+|\d+$/g, '').replace(/[^a-z]/g, ''))
        .filter(p => p.length > 0);
    if (parts.length === 0) {
        const letters = local.replace(/[^a-z]/g, '');
        return letters ? letters[0].toUpperCase() + letters.slice(1) : 'User';
    }
    const cap = parts.map(p => p[0].toUpperCase() + p.slice(1));
    return cap.length === 1 ? cap[0] : cap[0] + ' ' + cap[cap.length - 1];
}

// ══════════════════════════════════════════════════════════════════════════════
//  HOMEPAGE  (index.html) — Simple & Direct Connect
// ══════════════════════════════════════════════════════════════════════════════

function initHomepage() {
    // If already logged in, verify session and redirect to channels page
    if (getSessionToken()) {
        verifyExistingSession();
        return;
    }

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value.trim().toLowerCase();
            if (!email.includes('@')) {
                showError('Please enter a valid institution email.');
                return;
            }

            const btn = this.querySelector('button[type=submit]');
            btn.disabled = true;
            btn.textContent = 'Connecting...';

            try {
                const resp = await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email })
                });
                const data = await resp.json();
                if (data.status === 'ok') {
                    saveSession(data.token, data.displayName, data.email, data.role);
                    window.location.href = '/channels.html';
                } else {
                    showError(data.message || 'Unable to connect.');
                    btn.disabled = false;
                    btn.textContent = 'Connect to CampiFi';
                }
            } catch (err) {
                showError('Connection failed: ' + err.message);
                btn.disabled = false;
                btn.textContent = 'Connect to CampiFi';
            }
        });
    }
}

function verifyExistingSession() {
    fetch('/api/auth/check-session', {
        headers: { 'X-Session-Token': getSessionToken() }
    })
    .then(r => r.json())
    .then(data => {
        if (data.valid) {
            window.location.href = '/channels.html';
        } else {
            clearSession();
        }
    })
    .catch(() => clearSession());
}

// ══════════════════════════════════════════════════════════════════════════════
//  CHANNELS PAGE  (channels.html)
// ══════════════════════════════════════════════════════════════════════════════

let currentToken = null;
let pendingChannelId = null;
let pendingChannelName = null;

async function initChannelsPage() {
    const token = getSessionToken();
    if (!token) { window.location.href = '/'; return; }

    // Validate session
    let session;
    try {
        const resp = await fetch('/api/auth/check-session', { headers: { 'X-Session-Token': token } });
        const data = await resp.json();
        if (!data.valid) { clearSession(); window.location.href = '/'; return; }
        session = data;
    } catch { clearSession(); window.location.href = '/'; return; }

    currentToken = token;

    // Populate topbar
    document.getElementById('userBadge').textContent = session.displayName;
    const rb = document.getElementById('roleBadge');
    rb.textContent = session.role === 'ADMIN' ? 'Admin' : 'Member';
    rb.className = 'role-badge ' + (session.role === 'ADMIN' ? 'admin' : 'user');

    // Logout
    document.getElementById('logoutBtn').addEventListener('click', () => {
        fetch('/api/auth/logout', { method: 'POST', headers: { 'X-Session-Token': token } })
            .finally(() => { clearSession(); window.location.href = '/'; });
    });

    // Load networks
    await loadNetworks(token);
    setupPinModal(token);

    // Back button
    document.getElementById('subPanelBackBtn').addEventListener('click', () => {
        document.getElementById('subNetworkView').style.display = 'none';
        document.getElementById('networkView').style.display = 'block';
    });
}

async function loadNetworks(token) {
    const grid = document.getElementById('networkGrid');
    grid.innerHTML = '<div class="ch-loading"><div class="ch-loading-icon"></div></div>';

    try {
        const resp = await fetch('/api/channels', { headers: { 'X-Session-Token': token } });
        const data = await resp.json();

        if (!data.channels || data.channels.length === 0) {
            grid.innerHTML = '<p class="no-networks">No networks available yet. Check back later!</p>';
            return;
        }

        grid.innerHTML = '';
        data.channels.forEach(ch => grid.appendChild(buildNetworkCard(ch, token)));
    } catch {
        grid.innerHTML = '<p class="no-networks">Could not load networks. Please refresh.</p>';
    }
}

function buildNetworkCard(ch, token) {
    const card = document.createElement('div');
    card.className = 'network-card ' + (ch.type === 'PUBLIC' ? 'network-public' : 'network-private');

    const typeLabel  = ch.type === 'PUBLIC' ? 'Public' : 'Private';
    const members    = ch.memberCount + ' member' + (ch.memberCount !== 1 ? 's' : '');
    const subText    = ch.subChannelCount + ' sub-network' + (ch.subChannelCount !== 1 ? 's' : '');
    const btnLabel   = ch.type === 'PUBLIC' ? 'View' : 'Join';
    const btnClass   = ch.type === 'PUBLIC' ? 'btn-secondary' : 'btn-admin';

    card.innerHTML = `
        <div class="network-card-top">
            <span class="network-type-badge ${ch.type.toLowerCase()}">${typeLabel}</span>
        </div>
        <h3 class="network-name">${escapeHtml(ch.name)}</h3>
        <p class="network-desc">${escapeHtml(ch.description || '')}</p>
        <div class="network-meta">
            <span>${members}</span>
            <span>${subText}</span>
        </div>
        <button class="btn ${btnClass} network-btn">${btnLabel}</button>
    `;

    card.querySelector('button').addEventListener('click', () => {
        if (ch.type === 'PUBLIC') openPublicNetwork(ch.id, ch.name, token);
        else openPinModal(ch.id, ch.name, token);
    });

    return card;
}

async function openPublicNetwork(channelId, channelName, token) {
    await fetch('/api/channels/' + channelId + '/join', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Session-Token': token },
        body: JSON.stringify({})
    });
    const r = await fetch('/api/channels/' + channelId + '/sub-channels', {
        headers: { 'X-Session-Token': token }
    });
    const d = await r.json();
    showSubNetworks(channelId, channelName, d.subChannels || [], token, true);
}

// ── PIN modal ────────────────────────────────────────────────────────────────

function setupPinModal(token) {
    document.getElementById('pinCancelBtn').addEventListener('click', closePinModal);
    document.getElementById('pinModal').addEventListener('click', e => {
        if (e.target.id === 'pinModal') closePinModal();
    });

    document.getElementById('pinSubmitBtn').addEventListener('click', async () => {
        const pin = getPinValue();
        if (pin.length < 4) { showPinError('Please enter all 4 digits.'); return; }

        const btn = document.getElementById('pinSubmitBtn');
        btn.disabled = true; btn.textContent = 'Verifying...';

        try {
            const resp = await fetch('/api/channels/' + pendingChannelId + '/join', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-Session-Token': token },
                body: JSON.stringify({ pin })
            });
            const data = await resp.json();

            if (data.status === 'ok') {
                closePinModal();
                showSubNetworks(pendingChannelId, pendingChannelName, data.subChannels || [], token, false);
            } else {
                showPinError(data.message || 'Incorrect PIN. Try again.');
                shakePinBoxes();
                clearPinBoxes();
                btn.disabled = false; btn.textContent = 'Enter Network';
            }
        } catch (err) {
            showPinError('Error: ' + err.message);
            btn.disabled = false; btn.textContent = 'Enter Network';
        }
    });

    setupPinBoxes();
}

function openPinModal(channelId, channelName) {
    pendingChannelId   = channelId;
    pendingChannelName = channelName;
    document.getElementById('pinModalTitle').textContent = channelName;
    document.getElementById('pinModalSub').textContent   = 'Enter the 4-digit PIN to join this private network.';
    document.getElementById('pinError').style.display    = 'none';
    document.getElementById('pinSubmitBtn').disabled      = false;
    document.getElementById('pinSubmitBtn').textContent   = 'Enter Network';
    clearPinBoxes();
    document.getElementById('pinModal').style.display     = 'flex';
    setTimeout(() => document.querySelector('#pinBoxes .otp-box').focus(), 80);
}
function closePinModal() {
    document.getElementById('pinModal').style.display = 'none';
    clearPinBoxes(); pendingChannelId = null; pendingChannelName = null;
}

function setupPinBoxes() {
    const boxes = document.querySelectorAll('#pinBoxes .otp-box');
    boxes.forEach((box, i) => {
        box.value = ''; box.classList.remove('filled');
        box.oninput = () => {
            box.value = box.value.replace(/[^0-9]/g, '').slice(-1);
            box.classList.toggle('filled', box.value !== '');
            if (box.value && i < boxes.length - 1) boxes[i + 1].focus();
        };
        box.onkeydown = e => {
            if (e.key === 'Backspace' && !box.value && i > 0) boxes[i - 1].focus();
            if (e.key === 'Enter') document.getElementById('pinSubmitBtn').click();
        };
        box.onpaste = e => {
            const p = e.clipboardData.getData('text').replace(/[^0-9]/g, '').slice(0, 4);
            if (p) {
                e.preventDefault();
                [...p].forEach((ch, j) => {
                    if (boxes[j]) { boxes[j].value = ch; boxes[j].classList.add('filled'); }
                });
                boxes[Math.min(p.length, boxes.length - 1)].focus();
            }
        };
    });
}
function getPinValue()   { return [...document.querySelectorAll('#pinBoxes .otp-box')].map(b => b.value).join(''); }
function clearPinBoxes() { document.querySelectorAll('#pinBoxes .otp-box').forEach(b => { b.value = ''; b.classList.remove('filled'); }); }
function shakePinBoxes() { const c = document.getElementById('pinBoxes'); if (!c) return; c.style.animation = 'none'; c.offsetHeight; c.style.animation = 'shake 0.4s ease'; }
function showPinError(msg) { const el = document.getElementById('pinError'); el.textContent = msg; el.style.display = 'block'; }

// ── Sub-network panel ─────────────────────────────────────────────────────────

function showSubNetworks(channelId, channelName, subChannels, token, readOnly) {
    document.getElementById('networkView').style.display     = 'none';
    document.getElementById('subNetworkView').style.display  = 'block';

    document.getElementById('subPanelTitle').textContent = channelName;
    document.getElementById('subPanelSub').textContent   = readOnly
        ? 'Public broadcast network — view updates and announcements.'
        : 'Select a sub-network to open the chat.';

    const list = document.getElementById('subNetworkList');
    list.innerHTML = '';

    if (!subChannels || subChannels.length === 0) {
        const item = buildSubItem('General', 'Open channel feed', readOnly);
        item.addEventListener('click', () => goToChat(channelId, null, channelName));
        list.appendChild(item);
    } else {
        subChannels.forEach(sub => {
            const item = buildSubItem(sub.name, sub.description || '', readOnly);
            item.addEventListener('click', () => goToChat(channelId, sub.id, sub.name));
            list.appendChild(item);
        });
    }
}

function buildSubItem(name, desc, readOnly) {
    const item = document.createElement('div');
    item.className = 'sub-item';
    item.innerHTML = `
        <div class="sub-item-left">
            <span class="sub-item-name">${escapeHtml(name)}</span>
            ${desc ? `<span class="sub-item-desc">${escapeHtml(desc)}</span>` : ''}
        </div>
        <span class="sub-item-arrow">&#8250;</span>
    `;
    return item;
}

function goToChat(channelId, subChannelId, name) {
    const user = getSessionName() || 'User';
    let url = '/chat.html?room=' + encodeURIComponent(name) + '&user=' + encodeURIComponent(user);
    if (channelId)    url += '&channelId='    + channelId;
    if (subChannelId) url += '&subChannelId=' + subChannelId;
    window.location.href = url;
}

// ══════════════════════════════════════════════════════════════════════════════
//  ADMIN DASHBOARD  (admin.html) — Networks, Dropdown Subchannels & Admins
// ══════════════════════════════════════════════════════════════════════════════

let addSubTargetChannelId = null;
let currentAdminTargetType = null; // 'channel' or 'subChannel'
let currentAdminTargetId   = null;

function initAdminDashboard() {
    // Sidebar navigation
    document.querySelectorAll('.admin-nav-item').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.admin-nav-item').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.querySelectorAll('.admin-section-content').forEach(s => s.style.display = 'none');
            document.getElementById('section-' + btn.dataset.section).style.display = 'block';
        });
    });

    // Show/hide create form
    document.getElementById('showCreateFormBtn').addEventListener('click', () => {
        const form = document.getElementById('createNetworkForm');
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
        document.getElementById('createMsg').textContent = '';
    });
    document.getElementById('cancelCreateBtn').addEventListener('click', () => {
        document.getElementById('createNetworkForm').style.display = 'none';
    });

    // Toggle PIN input visibility based on network type
    document.getElementById('networkType').addEventListener('change', function() {
        document.getElementById('pinInputRow').style.display =
            this.value === 'PRIVATE' ? 'block' : 'none';
    });

    // Create network
    document.getElementById('createNetworkBtn').addEventListener('click', createNetwork);

    // Add sub-network modal
    document.getElementById('cancelSubBtn').addEventListener('click', () => {
        document.getElementById('addSubModal').style.display = 'none';
    });
    document.getElementById('addSubModal').addEventListener('click', e => {
        if (e.target.id === 'addSubModal') document.getElementById('addSubModal').style.display = 'none';
    });
    document.getElementById('addSubBtn').addEventListener('click', addSubNetwork);

    // Manage Admins modal
    document.getElementById('closeAdminModalBtn').addEventListener('click', () => {
        document.getElementById('manageAdminsModal').style.display = 'none';
    });
    document.getElementById('manageAdminsModal').addEventListener('click', e => {
        if (e.target.id === 'manageAdminsModal') document.getElementById('manageAdminsModal').style.display = 'none';
    });
    document.getElementById('saveAdminBtn').addEventListener('click', saveAdminFromModal);

    // User role directory
    document.getElementById('promoteBtn').addEventListener('click', () => {
        const email = document.getElementById('promoteEmail').value.trim();
        if (!email) return;
        manageUserRole(email, 'promote', 'promoteMsg');
    });
    document.getElementById('demoteBtn').addEventListener('click', () => {
        const email = document.getElementById('demoteEmail').value.trim();
        if (!email) return;
        manageUserRole(email, 'demote', 'demoteMsg');
    });

    // Load networks list
    loadAdminNetworks();
}

async function loadAdminNetworks() {
    const list = document.getElementById('adminNetworkList');
    list.innerHTML = '<div class="ch-loading"><div class="ch-loading-icon"></div></div>';

    try {
        const resp = await fetch('/api/admin/channels');
        const data = await resp.json();

        if (data.status !== 'ok' || !data.channels.length) {
            list.innerHTML = '<p class="no-networks">No networks yet. Create one above!</p>';
            return;
        }

        list.innerHTML = '';
        data.channels.forEach(ch => list.appendChild(buildAdminNetworkItem(ch)));
    } catch {
        list.innerHTML = '<p class="no-networks">Could not load networks.</p>';
    }
}

function buildAdminNetworkItem(ch) {
    const item = document.createElement('div');
    item.className = 'admin-network-item';
    item.dataset.channelId = ch.id;

    const typeBadge = `<span class="network-type-badge ${ch.type.toLowerCase()}">${ch.type === 'PUBLIC' ? 'Public' : 'Private'}</span>`;
    const subInfo   = `<span>${ch.subChannelCount} sub-network(s)</span>`;

    item.innerHTML = `
        <div class="admin-network-header">
            <div class="admin-network-title">
                <button class="expand-toggle" title="Toggle sub-channels view">&#9654;</button>
                ${typeBadge}
                <strong class="admin-network-name">${escapeHtml(ch.name)}</strong>
            </div>
            <div class="admin-network-actions">
                <button class="btn-sm btn-admin-manage" data-id="${ch.id}" data-name="${escapeHtml(ch.name)}" title="Manage Master Admins for this entire network">Admins</button>
                <button class="btn-sm btn-add-sub" data-id="${ch.id}" data-name="${escapeHtml(ch.name)}">+ Sub-Network</button>
                <button class="btn-sm btn-danger btn-delete-ch" data-id="${ch.id}" data-name="${escapeHtml(ch.name)}">Delete</button>
            </div>
        </div>
        ${ch.description ? `<p class="admin-network-desc">${escapeHtml(ch.description)}</p>` : ''}
        <div class="admin-network-meta">${ch.memberCount} member(s) &bull; ${subInfo}</div>
        
        <!-- Dropdown container for sub-channels -->
        <div class="admin-expand-panel" id="dropdown-${ch.id}" style="display:none;">
            <div class="expand-section-title">Sub-Channels in ${escapeHtml(ch.name)}</div>
            <div class="expand-sub-list" id="sub-list-${ch.id}">
                <div class="ch-loading"><div class="ch-loading-icon" style="width:20px;height:20px;margin:0 auto 6px;"></div></div>
            </div>
        </div>
    `;

    // Expand toggle icon (drop down view of sub-channels)
    const toggleBtn = item.querySelector('.expand-toggle');
    const dropdown = item.querySelector(`#dropdown-${ch.id}`);
    toggleBtn.addEventListener('click', () => {
        const isOpen = dropdown.style.display !== 'none';
        if (isOpen) {
            dropdown.style.display = 'none';
            toggleBtn.innerHTML = '&#9654;'; // right arrow
        } else {
            dropdown.style.display = 'block';
            toggleBtn.innerHTML = '&#9660;'; // down arrow
            loadAdminSubNetworks(ch.id, item);
        }
    });

    // Root Master Admins modal
    item.querySelector('.btn-admin-manage').addEventListener('click', function() {
        openManageAdminsModal('channel', parseInt(this.dataset.id), this.dataset.name);
    });

    // Delete channel
    item.querySelector('.btn-delete-ch').addEventListener('click', async function() {
        if (!confirm('Delete network "' + this.dataset.name + '"? This will remove all sub-networks and chats.')) return;
        await fetch('/api/admin/channels/' + this.dataset.id, { method: 'DELETE' });
        loadAdminNetworks();
    });

    // Add sub-network
    item.querySelector('.btn-add-sub').addEventListener('click', function() {
        addSubTargetChannelId = parseInt(this.dataset.id);
        document.getElementById('addSubParentName').textContent = this.dataset.name;
        document.getElementById('subNetworkName').value = '';
        document.getElementById('subNetworkDesc').value = '';
        document.getElementById('addSubMsg').textContent = '';
        document.getElementById('addSubModal').style.display = 'flex';
    });

    return item;
}

async function loadAdminSubNetworks(channelId, parentItem) {
    const subList = parentItem.querySelector('#sub-list-' + channelId);
    if (!subList) return;

    try {
        const resp = await fetch('/api/admin/channels/' + channelId + '/sub-channels');
        const data = await resp.json();
        const subs = data.subChannels || [];

        if (subs.length === 0) {
            subList.innerHTML = '<p class="no-admin-text">No sub-channels yet. Click "+ Sub-Network" above to add one.</p>';
            return;
        }

        subList.innerHTML = '';
        subs.forEach(sub => {
            const row = document.createElement('div');
            row.className = 'expand-sub-row';
            row.innerHTML = `
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="expand-sub-info">
                        <strong style="font-size:0.92rem; color:var(--text);">${escapeHtml(sub.name)}</strong>
                        ${sub.description ? `<span style="font-size:0.8rem; color:var(--muted);">${escapeHtml(sub.description)}</span>` : ''}
                    </div>
                    <div style="display:flex; gap:8px; align-items:center;">
                        <button class="btn-sm btn-admin-manage btn-sub-admin" data-id="${sub.id}" data-name="${escapeHtml(sub.name)}">Admins</button>
                        <button class="btn-sm btn-danger btn-delete-sub" data-id="${sub.id}" data-name="${escapeHtml(sub.name)}">Remove</button>
                    </div>
                </div>
            `;

            // Sub-channel Admins button
            row.querySelector('.btn-sub-admin').addEventListener('click', function() {
                openManageAdminsModal('subChannel', parseInt(this.dataset.id), this.dataset.name);
            });

            // Delete sub-channel
            row.querySelector('.btn-delete-sub').addEventListener('click', async function() {
                if (!confirm('Remove sub-network "' + this.dataset.name + '"?')) return;
                await fetch('/api/admin/sub-channels/' + this.dataset.id, { method: 'DELETE' });
                loadAdminSubNetworks(channelId, parentItem);
            });

            subList.appendChild(row);
        });
    } catch {
        subList.innerHTML = '<p class="no-admin-text">Failed to load sub-channels.</p>';
    }
}

// ── Manage Admins Modal ───────────────────────────────────────────────────────

async function openManageAdminsModal(type, targetId, targetName) {
    currentAdminTargetType = type;
    currentAdminTargetId   = targetId;

    const modal = document.getElementById('manageAdminsModal');
    const title = document.getElementById('adminModalTitle');
    const sub   = document.getElementById('adminModalSub');
    const msg   = document.getElementById('adminModalMsg');
    const input = document.getElementById('newAdminEmail');

    input.value = '';
    msg.textContent = '';

    if (type === 'channel') {
        title.textContent = 'Master Admins — ' + targetName;
        sub.textContent   = 'Master Admins have full administrative authority over this root network and all of its sub-channels.';
    } else {
        title.textContent = 'Sub-Channel Admins — ' + targetName;
        sub.textContent   = 'Assigned Admins have moderation authority within this sub-channel.';
    }

    modal.style.display = 'flex';
    await loadCurrentAdmins();
    input.focus();
}

async function loadCurrentAdmins() {
    const list = document.getElementById('currentAdminsList');
    list.innerHTML = '<div class="ch-loading" style="padding:10px 0;"><div class="ch-loading-icon" style="width:20px;height:20px;margin:0 auto;"></div></div>';

    const url = currentAdminTargetType === 'channel'
        ? '/api/admin/channels/' + currentAdminTargetId + '/admins'
        : '/api/admin/sub-channels/' + currentAdminTargetId + '/admins';

    try {
        const resp = await fetch(url);
        const data = await resp.json();
        const admins = data.admins || [];

        if (admins.length === 0) {
            list.innerHTML = '<p class="no-admin-text">No admins assigned yet.</p>';
            return;
        }

        list.innerHTML = '';
        admins.forEach(admin => {
            const row = document.createElement('div');
            row.className = 'admin-user-row';
            row.innerHTML = `
                <div class="admin-user-info">
                    <span class="admin-user-name">${escapeHtml(admin.displayName)}</span>
                    <span class="admin-user-email">${escapeHtml(admin.email)}</span>
                </div>
                <button class="btn-sm btn-danger btn-remove-admin" data-id="${admin.userId}" data-email="${escapeHtml(admin.email)}">Remove</button>
            `;

            row.querySelector('.btn-remove-admin').addEventListener('click', async function() {
                const uid = this.dataset.id;
                const deleteUrl = currentAdminTargetType === 'channel'
                    ? '/api/admin/channels/' + currentAdminTargetId + '/admins/' + uid
                    : '/api/admin/sub-channels/' + currentAdminTargetId + '/admins/' + uid;

                await fetch(deleteUrl, { method: 'DELETE' });
                await loadCurrentAdmins();
            });

            list.appendChild(row);
        });
    } catch {
        list.innerHTML = '<p class="no-admin-text">Could not load admins list.</p>';
    }
}

async function saveAdminFromModal() {
    const input = document.getElementById('newAdminEmail');
    const email = input.value.trim().toLowerCase();
    const msg   = document.getElementById('adminModalMsg');

    if (!email || !email.includes('@')) {
        msg.textContent = 'Please enter a valid institution email.';
        msg.style.color = 'var(--error)';
        return;
    }

    const btn = document.getElementById('saveAdminBtn');
    btn.disabled = true;
    btn.textContent = 'Adding...';

    const url = currentAdminTargetType === 'channel'
        ? '/api/admin/channels/' + currentAdminTargetId + '/admins'
        : '/api/admin/sub-channels/' + currentAdminTargetId + '/admins';

    try {
        const resp = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await resp.json();

        if (data.status === 'ok') {
            msg.textContent = data.message || 'Admin assigned successfully.';
            msg.style.color = 'var(--accent)';
            input.value = '';
            await loadCurrentAdmins();
        } else {
            msg.textContent = data.message || 'Error assigning admin.';
            msg.style.color = 'var(--error)';
        }
    } catch (err) {
        msg.textContent = 'Error: ' + err.message;
        msg.style.color = 'var(--error)';
    }

    btn.disabled = false;
    btn.textContent = 'Add Admin';
}

async function createNetwork() {
    const name = document.getElementById('networkName').value.trim();
    const desc = document.getElementById('networkDesc').value.trim();
    const type = document.getElementById('networkType').value;
    const pin  = document.getElementById('networkPin')?.value.trim() || '';
    const msg  = document.getElementById('createMsg');

    if (!name) { msg.textContent = 'Network name is required.'; msg.style.color = 'var(--error)'; return; }
    if (type === 'PRIVATE' && !/^\d{4}$/.test(pin)) {
        msg.textContent = 'Please enter a valid 4-digit PIN.'; msg.style.color = 'var(--error)'; return;
    }

    const btn = document.getElementById('createNetworkBtn');
    btn.disabled = true; btn.textContent = 'Creating...';

    try {
        const resp = await fetch('/api/admin/channels', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description: desc, type, pin })
        });
        const data = await resp.json();

        if (data.status === 'ok') {
            msg.textContent = '"' + data.channelName + '" created!';
            msg.style.color = 'var(--accent)';
            document.getElementById('networkName').value = '';
            document.getElementById('networkDesc').value = '';
            if (document.getElementById('networkPin')) document.getElementById('networkPin').value = '';
            setTimeout(() => { document.getElementById('createNetworkForm').style.display = 'none'; msg.textContent = ''; }, 1200);
            loadAdminNetworks();
        } else {
            msg.textContent = data.message; msg.style.color = 'var(--error)';
        }
    } catch (err) { msg.textContent = 'Error: ' + err.message; msg.style.color = 'var(--error)'; }

    btn.disabled = false; btn.textContent = 'Create Network';
}

async function addSubNetwork() {
    const name = document.getElementById('subNetworkName').value.trim();
    const desc = document.getElementById('subNetworkDesc').value.trim();
    const msg  = document.getElementById('addSubMsg');

    if (!name) { msg.textContent = 'Sub-network name is required.'; msg.style.color = 'var(--error)'; return; }

    const btn = document.getElementById('addSubBtn');
    btn.disabled = true; btn.textContent = 'Adding...';

    try {
        const resp = await fetch('/api/admin/channels/' + addSubTargetChannelId + '/sub-channels', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, description: desc })
        });
        const data = await resp.json();

        if (data.status === 'ok') {
            msg.textContent = '"' + data.subChannelName + '" added!';
            msg.style.color = 'var(--accent)';
            setTimeout(() => { document.getElementById('addSubModal').style.display = 'none'; msg.textContent = ''; }, 1000);
            loadAdminNetworks();
        } else { msg.textContent = data.message; msg.style.color = 'var(--error)'; }
    } catch (err) { msg.textContent = 'Error: ' + err.message; msg.style.color = 'var(--error)'; }

    btn.disabled = false; btn.textContent = 'Add Sub-Network';
}

async function manageUserRole(email, action, msgElId) {
    const msg = document.getElementById(msgElId);
    try {
        const resp = await fetch('/api/admin/users/' + encodeURIComponent(email) + '/' + action, { method: 'PUT' });
        const data = await resp.json();
        msg.textContent = data.message;
        msg.style.color = data.status === 'ok' ? 'var(--accent)' : 'var(--error)';
    } catch (err) { msg.textContent = 'Error: ' + err.message; msg.style.color = 'var(--error)'; }
}

// ══════════════════════════════════════════════════════════════════════════════
//  CHAT PAGE  (chat.html)
// ══════════════════════════════════════════════════════════════════════════════

let stompClient = null;
let currentRoom = null;
let currentUser = null;

function initChat(room, user) {
    currentRoom = room;
    currentUser = user;
    document.getElementById('roomName').textContent = room;

    // ── STOMP / WebSocket ─────────────────────────────────────────────────
    const socket = new SockJS('/ws');
    stompClient  = Stomp.over(socket);
    stompClient.debug = null;

    stompClient.connect({}, function() {
        document.getElementById('chatMessages').innerHTML = '';
        stompClient.subscribe('/topic/room/' + room, function(message) {
            displayMessage(JSON.parse(message.body));
        });
        stompClient.send('/app/chat/' + room, {}, JSON.stringify({
            type: 'JOIN', sender: user, content: user + ' joined', room
        }));
        addSystemMessage('Connected to ' + room);
        refreshMembers();
    }, function() {
        addSystemMessage('Connection lost. Refresh to reconnect.');
    });

    // ── Text send ─────────────────────────────────────────────────────────
    document.getElementById('messageForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const input   = document.getElementById('messageInput');
        const content = input.value.trim();
        if (content && stompClient && stompClient.connected) {
            stompClient.send('/app/chat/' + room, {}, JSON.stringify({
                type: 'CHAT', sender: user, content, room
            }));
            input.value = '';
        }
    });

    // ── Paperclip button ──────────────────────────────────────────────────
    const paperclipBtn = document.getElementById('paperclipBtn');
    const fileInput    = document.getElementById('fileInput');

    if (paperclipBtn && fileInput) {
        paperclipBtn.addEventListener('click', () => {
            try { fileInput.click(); } catch(e) {}
        });

        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                uploadAndSend(this.files[0], room, user);
                this.value = '';
            }
        });
    }

    // ── Drag & Drop support ───────────────────────────────────────────────
    const dropZone = document.querySelector('.chat-container') || document.body;
    dropZone.addEventListener('dragover', e => { e.preventDefault(); e.stopPropagation(); });
    dropZone.addEventListener('drop', e => {
        e.preventDefault();
        e.stopPropagation();
        if (e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0]) {
            uploadAndSend(e.dataTransfer.files[0], room, user);
        }
    });

    // ── Paste image support ───────────────────────────────────────────────
    document.addEventListener('paste', function(e) {
        const items = e.clipboardData && e.clipboardData.items;
        if (!items) return;
        for (const item of items) {
            if (item.type.startsWith('image/')) {
                e.preventDefault();
                const file = item.getAsFile();
                if (file) uploadAndSend(file, room, user);
                break;
            }
        }
    });

    setInterval(refreshMembers, 10000);
}

// ── Upload then broadcast ─────────────────────────────────────────────────────

function uploadAndSend(file, room, user) {
    if (!file) return;
    const token = sessionStorage.getItem('campifi_token') || '';

    const progressBar  = document.getElementById('uploadProgressBar');
    const progressFill = document.getElementById('uploadProgressFill');
    const statusRow    = document.getElementById('uploadStatusRow');
    const statusText   = document.getElementById('uploadStatusText');

    if (progressBar)  progressBar.style.display = 'block';
    if (statusRow)    statusRow.style.display   = 'block';
    if (progressFill) progressFill.style.width  = '0%';
    if (statusText)   statusText.textContent    = 'Uploading ' + file.name + '…';

    const formData = new FormData();
    formData.append('file', file);

    const xhr = new XMLHttpRequest();

    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            const pct = Math.round((e.loaded / e.total) * 100);
            if (progressFill) progressFill.style.width = pct + '%';
            if (statusText)   statusText.textContent   = 'Uploading… ' + pct + '%';
        }
    });

    xhr.addEventListener('load', function() {
        if (progressBar) progressBar.style.display = 'none';
        if (statusRow)   statusRow.style.display   = 'none';

        let data;
        try { data = JSON.parse(xhr.responseText); } catch { data = {}; }

        if (xhr.status === 200 && data.status === 'ok') {
            const fileMsg = {
                type:           'FILE',
                sender:         user,
                content:        file.name,
                room:           room,
                attachmentUrl:  data.url,
                attachmentName: data.name,
                attachmentType: data.type,
                attachmentSize: data.size
            };

            if (stompClient && stompClient.connected) {
                stompClient.send('/app/chat/' + room, {}, JSON.stringify(fileMsg));
            } else {
                displayMessage(fileMsg);
            }
        } else {
            const errMsg = data.message || ('Error ' + xhr.status);
            addSystemMessage('Upload failed: ' + errMsg);
            alert('Upload failed: ' + errMsg);
        }
    });

    xhr.addEventListener('error', function() {
        if (progressBar) progressBar.style.display = 'none';
        if (statusRow)   statusRow.style.display   = 'none';
        addSystemMessage('Upload failed — check your connection.');
        alert('Upload failed — check your network connection.');
    });

    xhr.open('POST', '/api/upload');
    if (token) xhr.setRequestHeader('X-Session-Token', token);
    xhr.send(formData);
}

// ── Render incoming messages ──────────────────────────────────────────────────

function displayMessage(msg) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;

    if (msg.type === 'JOIN' || msg.type === 'LEAVE') {
        addSystemMessage(msg.content);
        refreshMembers();
        return;
    }

    const isSelf = msg.sender === currentUser;
    const wrap   = document.createElement('div');
    wrap.className = 'message ' + (isSelf ? 'message-self' : 'message-other');

    let html = '';
    if (!isSelf) {
        html += '<div class="message-sender">' + escapeHtml(msg.sender) + '</div>';
    }

    if (msg.type === 'FILE' && msg.attachmentUrl) {
        const isImg = (msg.attachmentType === 'image') ||
                      (/\.(png|jpe?g|gif|webp|bmp|svg)$/i.test(msg.attachmentUrl || '')) ||
                      (/\.(png|jpe?g|gif|webp|bmp|svg)$/i.test(msg.attachmentName || ''));

        if (isImg) {
            html += '<div class="msg-image-wrap">'
                  + '<a href="' + escapeHtml(msg.attachmentUrl) + '" target="_blank" rel="noopener">'
                  + '<img class="msg-image" src="' + escapeHtml(msg.attachmentUrl) + '"'
                  + ' alt="' + escapeHtml(msg.attachmentName || 'image') + '" loading="lazy">'
                  + '</a>';
            if (msg.attachmentName) {
                html += '<div class="msg-image-caption">' + escapeHtml(msg.attachmentName) + '</div>';
            }
            html += '</div>';
        } else {
            const sizeLabel = msg.attachmentSize ? formatFileSize(msg.attachmentSize) : '';
            const icon      = fileIcon(msg.attachmentName || '');
            html += '<a class="msg-file-pill" href="' + escapeHtml(msg.attachmentUrl) + '"'
                  + ' target="_blank" rel="noopener" download="' + escapeHtml(msg.attachmentName || 'file') + '">'
                  + '<span class="msg-file-icon">' + icon + '</span>'
                  + '<span class="msg-file-info">'
                  + '<span class="msg-file-name">' + escapeHtml(msg.attachmentName || 'File') + '</span>'
                  + (sizeLabel ? '<span class="msg-file-size">' + sizeLabel + '</span>' : '')
                  + '</span>'
                  + '<span class="msg-file-dl">↓</span>'
                  + '</a>';
        }
    } else {
        html += '<div class="message-content">' + escapeHtml(msg.content) + '</div>';
    }

    html += '<div class="message-time">' + (msg.timestamp || '') + '</div>';
    wrap.innerHTML = html;
    chatMessages.appendChild(wrap);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addSystemMessage(text) {
    const chatMessages = document.getElementById('chatMessages');
    if (!chatMessages) return;
    const div = document.createElement('div');
    div.className   = 'system-message';
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function refreshMembers() {
    if (!currentRoom) return;
    fetch('/api/hotspot/members/' + encodeURIComponent(currentRoom))
        .then(r => r.json())
        .then(data => {
            if (data.members) {
                const el = document.getElementById('membersList');
                if (el) el.textContent = data.members.join(', ');
                const cnt = document.getElementById('memberCount');
                if (cnt) cnt.textContent = data.memberCount + ' member' + (data.memberCount !== 1 ? 's' : '');
            }
        })
        .catch(() => {});
}

function formatFileSize(bytes) {
    if (bytes < 1024)        return bytes + ' B';
    if (bytes < 1048576)     return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

function fileIcon(name) {
    const ext = (name.split('.').pop() || '').toLowerCase();
    const map = { pdf:'📄', doc:'📝', docx:'📝', xls:'📊', xlsx:'📊', ppt:'📑', pptx:'📑', zip:'🗜️', rar:'🗜️', txt:'📃' };
    return map[ext] || '📎';
}


window.addEventListener('beforeunload', function() {
    if (stompClient && stompClient.connected && currentRoom && currentUser) {
        stompClient.send('/app/chat/' + currentRoom, {}, JSON.stringify({
            type: 'LEAVE', sender: currentUser, content: currentUser + ' left', room: currentRoom
        }));
    }
});


// ══════════════════════════════════════════════════════════════════════════════
//  SHARED HELPERS
// ══════════════════════════════════════════════════════════════════════════════

function showError(msg) { const el = document.getElementById('errorMessage'); if (el) { el.textContent = msg; el.style.display = 'block'; } }
function clearError()   { const el = document.getElementById('errorMessage'); if (el) { el.style.display = 'none'; el.textContent = ''; } }

function escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = text || '';
    return d.innerHTML;
}

// Inject shake keyframe animation
const _shakeStyle = document.createElement('style');
_shakeStyle.textContent = `
@keyframes shake {
    0%,100% { transform: translateX(0); }
    20%      { transform: translateX(-6px); }
    40%      { transform: translateX(6px); }
    60%      { transform: translateX(-4px); }
    80%      { transform: translateX(4px); }
}`;
document.head.appendChild(_shakeStyle);
