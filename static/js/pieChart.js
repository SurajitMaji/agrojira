    // Get the canvas element
    const canvas = document.getElementById('pie-chart-canvas');
    const ctx = canvas.getContext('2d');
    
    // Define the pie chart data
    const data = [
      { label: 'Portion 1', value: 20 },
      { label: 'Portion 2', value: 30 },
      { label: 'Portion 3', value: 15 },
      { label: 'Portion 4', value: 25 },
      { label: 'Portion 5', value: 10 },
      { label: 'Portion 6', value: 20 }
    ];
    
    // Define the colors for each portion
    const colors = ['#FF69B4', '#33CC33', '#6666CC', '#CC3333', '#CCCC33', '#33CCCC'];
    
    // Calculate the total value of the pie chart
    const totalValue = data.reduce((acc, curr) => acc + curr.value, 0);
    
    // Draw the pie chart
    ctx.beginPath();
    ctx.arc(200, 200, 150, 0, 2 * Math.PI);
    ctx.fillStyle = '#fff';
    ctx.fill();
    
    // Draw each portion of the pie chart
    let startAngle = 0;
    data.forEach((portion, index) => {
      const endAngle = startAngle + (portion.value / totalValue) * 2 * Math.PI;
      ctx.beginPath();
      ctx.moveTo(200, 200);
      ctx.arc(200, 200, 150, startAngle, endAngle);
      ctx.fillStyle = colors[index];
      ctx.fill();
      startAngle = endAngle;
    });
    
    // Add labels for each portion
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    data.forEach((portion, index) => {
      const angle = (startAngle - (portion.value / totalValue) * Math.PI) + (portion.value / totalValue) * Math.PI;
      const x = 200 + Math.cos(angle) * 170;
      const y = 200 + Math.sin(angle) * 170;
      ctx.fillStyle = '#000';
      ctx.fillText(portion.label, x, y);
    });