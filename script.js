// Grab all dropdown wrappers on the page
const dropdownWrappers = document.querySelectorAll('.dropdown-wrapper');

dropdownWrappers.forEach(wrapper => {
    // Select the elements specific to *this* wrapper
    const toggleBtn = wrapper.querySelector('.js-dropdown-toggle');
    const dropdownMenu = wrapper.querySelector('.js-dropdown-menu');
    const categoryText = wrapper.querySelector('.category-text');
    const chevronIcon = wrapper.querySelector('.js-chevron-icon');
    const dropdownItems = wrapper.querySelectorAll('.dropdown-item');

    // Toggle open/close on button click
    toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation(); 
        
        // Optional: Close all *other* open dropdowns first for cleaner UX
        document.querySelectorAll('.js-dropdown-menu').forEach(menu => {
            if (menu !== dropdownMenu) menu.classList.remove('show');
        });
        document.querySelectorAll('.js-chevron-icon').forEach(icon => {
            if (icon !== chevronIcon) icon.classList.add('closed');
        });

        // Toggle the clicked dropdown
        dropdownMenu.classList.toggle('show');
        chevronIcon.classList.toggle('closed');
    });

    // Handle item selection inside this specific dropdown
    dropdownItems.forEach(item => {
        item.addEventListener('click', (e) => {
            categoryText.textContent = e.target.textContent;
            dropdownMenu.classList.remove('show');
            chevronIcon.classList.add('closed');
        });
    });
});

// Close any open dropdowns automatically when clicking outside
document.addEventListener('click', () => {
    document.querySelectorAll('.js-dropdown-menu').forEach(menu => menu.classList.remove('show'));
    document.querySelectorAll('.js-chevron-icon').forEach(icon => icon.classList.add('closed'));
});