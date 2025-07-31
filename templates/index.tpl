<!DOCTYPE html>
<html>
<head>
    <title>PocketGlide</title>
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-gray-900 font-sans max-w-4xl mx-auto p-4">

    <h1 class="text-3xl font-bold mb-6 text-center tracking-wide">PocketGlide</h1>


    <div class="flex flex-wrap justify-center gap-4 mb-6">
        <div class="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold shadow-sm">
            🕓 {{stats["airtime"] // 60}}h {{stats["airtime"] % 60}}m total
        </div>

        <div class="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-semibold shadow-sm">
            ✈️ {{stats["count"]}} flights
        </div>

        <div class="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-semibold shadow-sm">
            📆 {{stats["this_month"]}} flights this month
        </div>


    </div>


    <div class="bg-gray-50 border border-gray-200 rounded-xl p-5 mb-8 shadow-sm">
        <form action="/add" method="post" class="flex flex-wrap items-center gap-4 justify-center">
            
            <input name="date" type="date" value="{{today}}" 
                class="border px-2 py-1 rounded w-[130px]" placeholder="Date" required>

            <select name="plane_id" class="border px-2 py-1 rounded w-[300px]" required>
            <option disabled selected>Select plane</option>
            % for plane in planes:
                <option value="{{plane.doc_id}}">{{plane['type']}} ({{plane['registration']}})</option>
            % end
            </select>


            <div class="flex items-center">
            <input name="hours" type="number" min="0" placeholder="h"
                    class="border px-2 py-1 rounded w-[60px]" required>
            <span class="px-1 text-gray-600">:</span>
            <input name="minutes" type="number" min="0" max="59" placeholder="m"
                    class="border px-2 py-1 rounded w-[60px]" required>
            </div>


            <input name="airport" type="text" placeholder="ICAO" 
                class="border px-2 py-1 rounded w-[100px]" required>

            <button type="submit" 
                    class="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700">ADD</button>

        </form>
    </div>

    
    <div class="bg-gray-50 border border-gray-200 rounded-xl p-6 shadow-sm
                space-y-2 h-[calc(83vh-140px)] overflow-y-auto pt-0 px-6 pb-6">
    <h2 class="text-xl font-semibold mb-4 text-center sticky top-0 bg-gray-50 z-10 w-full py-2">Flight Log</h2>

    % for flight in flights:
    <div class="flex justify-between items-center border-b pb-2 text-sm text-gray-800">

        <div class="flex flex-col sm:flex-row sm:items-baseline sm:gap-3">
        <span class="font-mono text-gray-600">{{flight['date']}}</span>
        <span class="font-medium">{{flight['aircraft']}}</span>
        <span class="text-gray-500">{{flight['airport']}}</span>
        </div>

        <div class="text-right">
        <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-1 rounded">
            {{(flight['airtime'] // 60)}}h {{(flight['airtime'] % 60)}}m
        </span>
        </div>

    </div>
    % end
    </div>


    <div class="flex justify-between items-center text-xs text-gray-400 mt-4 leading-none">
        © Václav Šprincl 2025
        <button type="button" onclick="toggleAddPlane()" class="text-blue-600 hover:text-blue-800 underline ml-1">
            + Add plane
        </button>
    </div>



    <div id="addPlaneForm" class="hidden bg-gray-50 border border-gray-200 rounded-xl p-2 mb-8 shadow-sm">
        <form action="/add_plane" method="post" class="flex flex-wrap items-center gap-4 justify-center">
            <input name="type" type="text" placeholder="Type" 
                class="border px-2 py-1 rounded w-[200px]" required>
            
            <input name="registration" type="text" placeholder="Registration" 
                class="border px-2 py-1 rounded w-[100px]" required>

            <button type="submit" 
                    class="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700">Create</button>

        </form>
    </div>

    <script>
        function toggleAddPlane() {
            const form = document.getElementById('addPlaneForm');
            form.classList.toggle('hidden');
        }
    </script>
    





</body>
</html>
