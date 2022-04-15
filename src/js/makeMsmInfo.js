export let britishMsmInfo = {};
export let louvreMsmInfo = {};

export const makeMsmInfo = (britishSpawn, louvreSpawn) => {
  const britishMsmData = britishSpawn("python", [
    process.cwd() + "/src/pydata/infoCrawler.py",
  ]);
  const louvreMsmData = louvreSpawn("python", [
    process.cwd() + "/src/pydata/louvre.py",
  ]);

  const handleMsmData = (data) => {
    const dataStringList = [];
    let msmDataString = data.toString();
    let startIdx = 0;
    let idxOfFilter = 0;
    const FILTER = "FILTER";

    while (idxOfFilter !== -1) {
      idxOfFilter = msmDataString.indexOf(`${FILTER}`, startIdx);
      let dataString = msmDataString.slice(startIdx, idxOfFilter); // 가공안된거
      dataStringList.push(dataString);
      startIdx = idxOfFilter + `${FILTER}}`.length;
    }

    for (let i = 0; i < dataStringList.length; i += 1) {
      dataStringList[i] = dataStringList[i].split("//");
      for (let j = 0; j < dataStringList[i].length; j += 1) {
        dataStringList[i][j] = dataStringList[i][j].replace(/(\r\n\r\n)/gm, "");
      }
      dataStringList[i] = dataStringList[i].filter((el) => el !== "");
    }

    let msmInfo = {
      titles: dataStringList[0],
      dates: dataStringList[1],
    };
    console.log(msmInfo.titles);
    console.log(msmInfo.dates);

    return msmInfo;
  };
  britishMsmData.stdout.on("data", function (data) {
    // console.log(data.toString());
    britishMsmInfo = handleMsmData(data);
  });
  britishMsmData.stderr.on("data", function (data) {
    // console.log(data.toString());
  });

  louvreMsmData.stdout.on("data", function (data) {
    console.log(data.toString());
    louvreMsmInfo = handleMsmData(data);
  });
  louvreMsmData.stderr.on("data", function (data) {
    console.log(data.toString());
  });
};
