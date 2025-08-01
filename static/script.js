function enableEdit(id) {
    const row = document.getElementById(`row-${id}`);
    FetchFlight(id).then(data => {
        console.log('Data:', data);
            row.innerHTML = `
                <form action="/edit/${id}" method="post" class="flex gap-2 items-center text-sm py-2 border-b">
                    <input name="date" type="date" value="${data.date}" class="border px-2 py-1 rounded w-[130px]" required>
                    <input name="aircraft" type="text" value="${data.aircraft}" class="border px-2 py-1 rounded w-[200px]" required>
                    <input name="airport" type="text" value="${data.airport}" placeholder="ICAO" class="border px-2 py-1 rounded w-[100px]" required>
                    <input name="task" type="text" value="${data.task || ''}" placeholder="task" class="border px-2 py-1 rounded w-[80px]">
                    <input name="note" type="text" value="${data.notes || ''}" placeholder="notes" class="border px-2 py-1 rounded w-[150px]">
                    <input name="airtime" type="number" value="${data.airtime}" placeholder="time" class="border px-2 py-1 rounded w-[70px]" required>
                    <button type="submit" class="bg-blue-600 text-white px-3 py-1 rounded">💾</button>
                    <button type="button" onclick="location.reload()" class="text-gray-400 hover:text-black text-xs">✖️</button>
                </form>`
    });
}

async function FetchFlight(id) {
    const response = await fetch(`/get_flight/${id}`);
    const data = await response.json();
    return data;
}