const repoMap = [
  {repo: "ISYSLAB-HUST/DNARaptorQ", starId: "star-count-dna", updatedId: "updated-dna"},
  {repo: "ISYSLAB-HUST/ProtFlash", starId: "star-count-protflash", updatedId: "updated-protflash"},
  {repo: "ISYSLAB-HUST/DeepTMpred", starId: "star-count-tmpred", updatedId: "updated-tmpred"},
  {repo: "ISYSLAB-HUST/DeepNeuropePred", starId: "star-count-deepneurope", updatedId: "updated-deepneurope"},
  {repo: "ISYSLAB-HUST/NeuroPred-PLM", starId: "star-count-neuropred", updatedId: "updated-neuropred"},
  {repo: "ISYSLAB-HUST/Res-Dom", starId: "star-count-resdom", updatedId: "updated-resdom"}
];

repoMap.forEach(item => {
  // 获取star数
  fetch(`https://api.github.com/repos/${item.repo}`)
    .then(response => response.json())
    .then(data => {
      if (document.getElementById(item.starId)) {
        document.getElementById(item.starId).textContent = data.stargazers_count;
      }
    });
  // 获取最后一次commit时间
  fetch(`https://api.github.com/repos/${item.repo}/commits?per_page=1`)
    .then(response => response.json())
    .then(data => {
      if (document.getElementById(item.updatedId) && data && data[0]) {
        const date = new Date(data[0].commit.committer.date);
        const formatted = date.getFullYear() + '-' +
          String(date.getMonth() + 1).padStart(2, '0') + '-' +
          String(date.getDate()).padStart(2, '0');
        document.getElementById(item.updatedId).textContent = formatted;
      }
    });
}); 