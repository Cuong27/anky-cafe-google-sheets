const cases = 
[
    {
    no: 'AK—001',
    title: 'Vũ điệu dưới trăng',
    desc: 'Năm 2005, tại bản Nà Pha hẻo lánh thuộc vùng núi Lào Cai, sự mất tích bí ẩn của một cô gái vào đêm trăng sáng đã kéo theo những bí mật bị chôn giấu suốt nhiều năm. Giữa những lời đồn về hồ thiêng và những mối quan hệ đầy toan tính, liệu ai đang nói thật, ai đang che giấu tội lỗi, và sự thật nào sẽ được phơi bày?',
    meta: 'Khó · 5 người · 3–4 tiếng',
    price: '199.000đ/người'
}, {
    no: 'AK—002',
    title: 'Vết cắn lúc nửa đêm',
    desc: 'Giữa những màn hù dọa và hàng loạt bí mật ngoại tình, lừa tiền, thù hận dần bị phơi bày, ai mới là hung thủ thực sự đằng sau?',
    meta: 'Trung bình · 6 người · 2–3 tiếng',
    price: '159.000đ/người'
}, {
    no: 'AK—003',
    title: 'Bóng đêm lô cao su',
    desc: 'Lấy bối cảnh vụ án mạng có thật năm 2015 tại Tây Ninh, trò chơi đưa bạn vào cuộc đối chất sinh tử giữa 4 nghi phạm mang đầy mâu thuẫn tiền bạc và tình cảm với nạn nhân. Ai đang che giấu bí mật đen tối? Ai mới là hung thủ thực sự?',
    meta: 'Trung bình · 4 người · 2–3 tiếng',
    price: '159.000đ/người'
}, {
    no: 'AK—004',
    title: 'Đêm rằm tuyết trắng',
    desc: 'Chào mừng các bạn đến với biệt thự họ Trần tại đỉnh Tam Đảo. Đêm nay, bão tuyết phong tỏa toàn bộ ngọn núi, cắt đứt mọi liên lạc với bên ngoài. Phía sau cánh cửa gỗ lim dường như đã bị khóa chốt bên trong, Trần Lão Gia đã trút hơi thở cuối cùng bởi một sợi dây lụa bí ẩn. Hung thủ đang ngồi ngay tại bàn tròn này và hắn có quyền nói dối để biến các bạn thành kẻ thế mạng! Liệu sự thật sẽ bước ra ánh sáng, hay sẽ bị chôn vùi vĩnh viễn dưới lớp tuyết trắng đêm nay?',
    meta: 'Dễ · 5 người · 1–2 tiếng',
    price: '99.000đ/người'
}
];

const drinks = 
[
    // ================= CÀ PHÊ =================
    {
        id: 1,
        category: 'Cà phê',
        name: 'Hồ Sơ Đen',
        desc: 'Cà phê đen',
        price: 35000,
        icon: '☕'
    },
    {
        id: 2,
        category: 'Cà phê',
        name: 'Lời Khai Ngọt Ngào',
        desc: 'Cà phê sữa',
        price: 40000,
        icon: '🥛'
    },
    {
        id: 3,
        category: 'Cà phê',
        name: 'Lời Khai Nửa Thật',
        desc: 'Bạc xỉu',
        price: 40000,
        icon: '🥛'
    },
    {
        id: 4,
        category: 'Cà phê',
        name: 'Dấu Vết Cuối Cùng',
        desc: 'Cà phê muối',
        price: 45000,
        icon: '🧂'
    },
    {
        id: 5,
        category: 'Cà phê',
        name: 'Nhân Chứng Câm Lặng',
        desc: 'Americano',
        price: 45000,
        icon: '☕'
    },
    {
        id: 6,
        category: 'Cà phê',
        name: 'Kẻ Hai Mặt',
        desc: 'Latte',
        price: 45000,
        icon: '🥤'
    },

    // ================= TRÀ SỮA =================
    {
        id: 7,
        category: 'Trà sữa',
        name: 'Lời Khai Ban Đầu',
        desc: 'Trà sữa Ẩn Ký',
        price: 45000,
        icon: '🧋'
    },
    {
        id: 8,
        category: 'Trà sữa',
        name: 'Bí Mật Hắc Ám',
        desc: 'Trà sữa socola',
        price: 45000,
        icon: '🍫'
    },
    {
        id: 9,
        category: 'Trà sữa',
        name: 'Mật Mã Hoa Hồng(Signature)',
        desc: 'Trà sữa hoa hồng',
        price: 55000,
        icon: '🌹'
    },
    {
        id: 10,
        category: 'Trà sữa',
        name: 'Lớp Mặt Nạ',
        desc: 'Trà sữa ngô chiên kem cheese',
        price: 55000,
        icon: '🧀'
    },
    {
        id: 11,
        category: 'Trà sữa',
        name: 'Mắt Quỷ(Signature)',
        desc: 'Trà sữa bóng đêm',
        price: 55000,
        icon: '🌑'
    },
    {
        id: 12,
        category: 'Trà sữa',
        name: 'Cuộc Gọi Nặc Danh(Signature)',
        desc: 'Dừa hoa hồng',
        price: 55000,
        icon: '🥥'
    },

    // ================= TRÀ TRÁI CÂY =================
    {
        id: 13,
        category: 'Trà trái cây',
        name: 'Án Mạng Hoàng Hôn',
        desc: 'Trà xoài chanh leo',
        price: 50000,
        icon: '🥭'
    },
    {
        id: 14,
        category: 'Trà trái cây',
        name: 'Hung Khí(Signature)',
        desc: 'Trà hồng thạch',
        price: 55000,
        icon: '🫖'
    },
    {
        id: 15,
        category: 'Trà trái cây',
        name: 'Chứng Cứ Ngoại Phạm(Signature)',
        desc: 'Trà sấu muối ớt',
        price: 50000,
        icon: '🌶️'
    },
    {
        id: 16,
        category: 'Trà trái cây',
        name: 'Khẩu Cung',
        desc: 'Trà mãng cầu',
        price: 50000,
        icon: '🍈'
    },
    {
        id: 17,
        category: 'Trà trái cây',
        name: 'Dấu Vân Tay',
        desc: 'Trà măng cụt',
        price: 50000,
        icon: '🍇'
    },
    {
        id: 18,
        category: 'Trà trái cây',
        name: 'Vùng Cấm(Signature)',
        desc: 'Hồng tắc lắc',
        price: 50000,
        icon: '🍊'
    },

    // ================= SODA =================
    {
        id: 19,
        category: 'Soda',
        name: 'Tang Chứng',
        desc: 'Soda vỏ cam chanh dây',
        price: 50000,
        icon: '🍹'
    },
    {
        id: 20,
        category: 'Soda',
        name: 'Đồng Phạm',
        desc: 'Soda chanh muối',
        price: 50000,
        icon: '🍋'
    },
    {
        id: 21,
        category: 'Soda',
        name: 'Manh Mối Giả',
        desc: 'Soda việt quất',
        price: 50000,
        icon: '🫐'
    },
    {
        id: 22,
        category: 'Soda',
        name: 'Nhân Chứng Đỏ',
        desc: 'Soda dâu',
        price: 50000,
        icon: '🍓'
    },
    {
        id: 23,
        category: 'Soda',
        name: 'Hiện Trường Vụ Án',
        desc: 'Soda chanh dây',
        price: 50000,
        icon: '🍹'
    },
    {
        id: 24,
        category: 'Soda',
        name: 'Kẻ Đứng Sau',
        desc: 'Soda xoài',
        price: 50000,
        icon: '🥭'
    }
];

let cart = {};
let activeCase = 0;
const fmt = n => new Intl.NumberFormat('vi-VN').format(n) + 'đ';
const menuGrid = document.getElementById('menuGrid');
menuGrid.innerHTML = drinks.map(d => `<article class="drink"><div class="drink-icon">${d.icon}</div><div class="drink-info"><h3>${d.name}</h3><p>${d.desc}</p><div class="drink-bottom"><span class="drink-price">${fmt(d.price)}</span><button class="add" data-add="${d.id}" aria-label="Thêm ${d.name}">+</button></div></div></article>`).join('');

function toast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(window.toastTimer);
    window.toastTimer = setTimeout(() => t.classList.remove('show'), 2500)
}

function openCase(i) {
    activeCase = i;
    const c = cases[i];
    document.getElementById('modalEyebrow').textContent = 'HỒ SƠ MẬT / ' + c.no;
    document.getElementById('modalTitle').textContent = c.title;
    document.getElementById('modalDesc').textContent = c.desc;
    document.getElementById('modalMeta').textContent = c.meta + ' · ' + c.price;
    document.getElementById('caseModal').classList.add('open')
}
document.querySelectorAll('[data-case]').forEach(b => b.addEventListener('click', () => openCase(+b.dataset.case)));
document.querySelectorAll('[data-close]').forEach(b => b.addEventListener('click', () => document.getElementById(b.dataset.close).classList.remove('open')));
document.getElementById('caseModal').addEventListener('click', e => {
    if (e.target.id === 'caseModal') e.currentTarget.classList.remove('open')
});
document.getElementById('caseInterest').addEventListener('click', () => {
    document.getElementById('caseModal').classList.remove('open');
    document.getElementById('booking').scrollIntoView({
        behavior: 'smooth'
    });
    toast('Đã chọn: ' + cases[activeCase].title + ' — hãy kết nối form đặt lịch khi triển khai.')
});

function renderCart() {
    const items = Object.entries(cart).filter(([id, q]) => q > 0);
    document.getElementById('cartCount').textContent = items.reduce((s, [id, q]) => s + q, 0);
    document.getElementById('cartItems').innerHTML = items.length ? items.map(([id, q]) => {
        const d = drinks.find(x => x.id === +id);
        return `<div class="cart-row"><div><strong>${d.name}</strong><small>${fmt(d.price)} / món</small></div><div class="qty"><button data-qty="${id}" data-delta="-1" aria-label="Giảm">−</button><span>${q}</span><button data-qty="${id}" data-delta="1" aria-label="Tăng">+</button></div></div>`
    }).join('') : '<div class="empty">Giỏ hàng đang trống.<br>Chọn một món từ thực đơn để bắt đầu.</div>';
    document.getElementById('cartTotal').textContent = fmt(items.reduce((s, [id, q]) => s + drinks.find(x => x.id === +id).price * q, 0));
    document.querySelectorAll('[data-qty]').forEach(b => b.addEventListener('click', () => {
        const id = b.dataset.qty;
        cart[id] = (cart[id] || 0) + (+b.dataset.delta);
        if (cart[id] <= 0) delete cart[id];
        renderCart()
    }))
}
menuGrid.addEventListener('click', e => {
    const b = e.target.closest('[data-add]');
    if (!b) return;
    const id = b.dataset.add;
    cart[id] = (cart[id] || 0) + 1;
    renderCart();
    toast('Đã thêm ' + drinks.find(d => d.id === +id).name + ' vào giỏ')
});
const panel = document.getElementById('cartPanel');
document.getElementById('openCart').addEventListener('click', () => {
    renderCart();
    panel.classList.add('open')
});
document.getElementById('closeCart').addEventListener('click', () => panel.classList.remove('open'));
document.getElementById('checkout').addEventListener('click', async () => {
    const items = Object.entries(cart).filter(([id, q]) => q > 0).map(([id, quantity]) => ({
        product_id: Number(id),
        quantity
    }));
    if (!items.length) {
        toast('Giỏ hàng đang trống.');
        return
    }
    const customer = document.getElementById('customerName').value.trim();
    const table = document.getElementById('tableNumber').value.trim();
    const orderType = document.getElementById('orderType').value;
    const button = document.getElementById('checkout');
    button.disabled = true;
    button.textContent = 'Đang gửi order…';
    try {
        const response = await fetch('/api/orders', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                customer_name: customer,
                table_number: table,
                order_type: orderType,
                items
            })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Không thể tạo order');
        toast('Đã gửi order · Tổng tiền ' + fmt(data.total));
        if (data.email_sent === false) {
            toast('Đơn đã lưu vào Sheet nhưng email chưa gửi được.')
        }
        cart = {};
        renderCart();
        document.getElementById('customerName').value = '';
        document.getElementById('tableNumber').value = '';
        panel.classList.remove('open')
    } catch (error) {
        toast(error.message || 'Lỗi kết nối máy chủ')
    } finally {
        button.disabled = false;
        button.textContent = 'Gửi order đến quầy'
    }
});
document.getElementById('bookingBtn').addEventListener('click', () => {
    toast('Khu vực đặt lịch đã được chừa sẵn — cần kết nối form/email/backend.');
});
document.getElementById('menuToggle').addEventListener('click', () => document.getElementById('navlinks').classList.toggle('show'));
document.querySelectorAll('#navlinks a').forEach(a => a.addEventListener('click', () => document.getElementById('navlinks').classList.remove('show')));
renderCart();