document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav-links");
  if (toggle && nav) toggle.addEventListener("click", () => { const open = nav.classList.toggle("open"); toggle.setAttribute("aria-expanded", String(open)); });
  document.querySelectorAll("[data-date-min]").forEach(input => { const now = new Date(); input.min = new Date(now.getTime()-now.getTimezoneOffset()*60000).toISOString().slice(0,10); });
  const swap = document.querySelector(".swap-button");
  if (swap) swap.addEventListener("click", () => { const form=swap.closest("form"), from=form.querySelector('[name="from"]'), to=form.querySelector('[name="to"]'); const value=from.value; from.value=to.value; to.value=value; });
  const sort=document.querySelector("#sort-buses"), list=document.querySelector("#bus-list");
  if(sort&&list) sort.addEventListener("change",()=>{ const cards=[...list.querySelectorAll(".bus-card")]; const mode=sort.value; cards.sort((a,b)=> mode==="price"?Number(a.dataset.price)-Number(b.dataset.price):mode==="departure"?a.dataset.departure.localeCompare(b.dataset.departure):mode==="rating"?Number(b.dataset.rating)-Number(a.dataset.rating):Number(a.dataset.price)-Number(b.dataset.price)); cards.forEach(card=>list.appendChild(card)); });
  const seats=document.querySelector("#seat-count"), total=document.querySelector("#estimated-total");
  if(seats&&total){const price=Number(total.dataset.price);const update=()=>total.textContent=`₹${price*Number(seats.value)}`;seats.addEventListener("change",update);update();}
  document.querySelectorAll(".copy-reference").forEach(button=>button.addEventListener("click",async()=>{try{await navigator.clipboard.writeText(button.dataset.copy);button.textContent="Copied!";}catch(error){window.prompt("Copy your booking reference:",button.dataset.copy);}}));
  document.querySelectorAll(".flash-close").forEach(button=>button.addEventListener("click",()=>button.closest(".flash").remove()));
});
