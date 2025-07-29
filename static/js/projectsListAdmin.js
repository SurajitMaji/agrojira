// const crops = [
//     {
//       name: "Wheat",
//       image: "https://via.placeholder.com/60",
//       season: "Winter",
//       duration: "120 days"
//     },
//     {
//       name: "Rice",
//       image: "https://via.placeholder.com/60",
//       season: "Monsoon",
//       duration: "150 days"
//     },
//     {
//       name: "Maize",
//       image: "https://via.placeholder.com/60",
//       season: "Summer",
//       duration: "90 days"
//     }
//   ];

//   const tbody = document.getElementById("crop-table-body");
//   crops.forEach((crop, index) => {
//     const row = document.createElement("tr");
//     row.innerHTML = `
//       <th scope="row">${index + 1}</th>
//       <td>${crop.name}</td>
//       <td><img src="${crop.image}" class="crop-img" alt="${crop.name}"></td>
//       <td>${crop.season}</td>
//       <td>${crop.duration}</td>
//       <td class="action-buttons">
//         <a href="#" class="action-button btn btn-sm btn-info text-white view"  onclick="viewCrop(1)">View</a>
//         <a href="#" class="action-button btn btn-sm btn-danger delete" onclick="deleteCrop(1)">Delete</a>
//       </td>
//     `;
//     tbody.appendChild(row);
//   });

  function viewCrop(id) {
      alert("Viewing crop with ID: " + id);
  }
  
  function deleteCrop(id) {
      if (confirm("Are you sure you want to delete crop with ID: " + id + "?")) {
          // Logic to delete the crop
          alert("Crop with ID: " + id + " deleted.");
      }
  }