function onOpen() {  
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Provas')
    .addItem('Criar prova', 'openForm')
    .addToUi();
}


function gerarNovaProva(scriptDropdown, nquest, sheetDropdown1, sheetDropdown2) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheetcontrole = ss.getSheetByName("Controle de Questões");
  var sheetfiltroprovas = ss.getSheetByName("Filtros - Provas");
  let lastrow = sheetcontrole.getLastRow();
  var pastaprovas = DriveApp.getFolderById("1RgzkM3XVlVuCyGi0A-rFCoeD_r2W7kGq");
  var pastaarquivos = DriveApp.getFolderById("1017L8oRpddI_H0jr2szLm0SxPdD7J_vr");
  let iddaprova = pastaprovas.getFilesByName(scriptDropdown).next().getId();
  let nomedaprova = scriptDropdown.substring(0,scriptDropdown.length-4);
  var gabaritodaprova = sendPdfToFlask(iddaprova);
  Logger.log(gabaritodaprova.length);
  
  

  nquest = gabaritodaprova.length;
  
  
  
  sheetcontrole.getRange(3,1,1,sheetcontrole.getLastColumn()).copyTo(sheetcontrole.getRange(lastrow+1,1,1,sheetcontrole.getLastColumn()), SpreadsheetApp.CopyPasteType.PASTE_NORMAL, false);
  sheetcontrole.getRange(lastrow+1,2).setValue(DriveApp.getFileById(iddaprova).getUrl());
  sheetcontrole.getRange(lastrow+1,3).setValue(nquest);
  sheetcontrole.getRange(lastrow+1,8).setFormula("=1-(COUNTBLANK(H"+(lastrow+2)+ ":H"+(lastrow+1+Number(nquest))+")/$C"+(lastrow+1)+")");
  sheetcontrole.getRange(lastrow+1,9).setFormula("=COUNTIF(I"+(lastrow+2)+":I"+(lastrow+1+Number(nquest))+";TRUE)/$C"+(lastrow+1));
  sheetcontrole.getRange(lastrow+1,18).setFormula("=COUNTIF(R"+(lastrow+2)+":R"+(lastrow+1+Number(nquest))+";TRUE)/$C"+(lastrow+1));
  sheetcontrole.getRange(lastrow+1,21).setFormula('=(C'+ (lastrow+1) +'-COUNTIF(U'+(lastrow+2)+':U'+(lastrow+1+Number(nquest))+';"Disponível"))/C'+(lastrow+1));
  sheetcontrole.getRange(lastrow+1,24).setFormula("=COUNTIF(X"+(lastrow+2)+":X"+(lastrow+1+Number(nquest))+";TRUE)/$C"+(lastrow+1));
  sheetcontrole.getRange(lastrow+1,42).setFormula("=COUNTIF(AP"+(lastrow+2)+":AP"+(lastrow+1+Number(nquest))+";"+'"Voltar")');
  sheetcontrole.getRange(lastrow+1,45).setFormula("=COUNTIF(AS"+(lastrow+2)+":AS"+(lastrow+1+Number(nquest))+";TRUE)/$C"+(lastrow+1));
  sheetcontrole.getRange(lastrow+1,49).setFormula("=COUNTIF(AW"+(lastrow+2)+":AW"+(lastrow+1+Number(nquest))+";"+'"Liberado para cadastro")');
  sheetcontrole.getRange(lastrow+1,57).setFormula("=COUNTIF(BE"+(lastrow+2)+":BE"+(lastrow+1+Number(nquest))+";TRUE)");
  sheetcontrole.getRange(lastrow+1,65).setFormula("=COUNTIF(BM"+(lastrow+2)+":BM"+(lastrow+1+Number(nquest))+";TRUE)/$C"+(lastrow+1));
  sheetcontrole.getRange(lastrow+1,75).setFormula('=(C'+ (lastrow+1) +'(-COUNTIF(BW'+(lastrow+2)+':BW'+(lastrow+1+Number(nquest))+';"Aprovada")+COUNTIF(BW'+(lastrow+2)+':BW'+(lastrow+1+Number(nquest))+';"")))');
  sheetcontrole.getRange(lastrow+1,76).setFormula("=COUNTIF(BX"+(lastrow+2)+":BX"+(lastrow+1+Number(nquest))+";TRUE)/$C"+(lastrow+1));
  
  
  let ano = scriptDropdown.toString().substring(0,4);
  let pastasdoano = pastaarquivos.getFoldersByName("PROVAS - "+ano);
  
  let primeirapasta = pastasdoano.next();
  let pastasdaprova = primeirapasta.getFoldersByName(nomedaprova);
  var iddapastadaprova = "";
  if(pastasdaprova.hasNext()){
    iddapastadaprova = pastasdaprova.next().getId();
    //return;
  }else{
    var pastanova = DriveApp.createFolder(nomedaprova);
    pastanova.moveTo(DriveApp.getFolderById(primeirapasta.getId()));
    iddapastadaprova = pastanova.getId();
  }
  let lastrowfilt = sheetfiltroprovas.getLastRow();
  sheetfiltroprovas.getRange(lastrowfilt+1,1).setValue(nomedaprova);
  var dia = new Date();
  sheetfiltroprovas.getRange(lastrowfilt+1,2).setValue(Utilities.formatDate(dia,"GMT-0300","dd/MM/yyyy"));
  sheetfiltroprovas.getRange(lastrowfilt+1,4).setFormula("='Controle de Questões'!H"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,5).setFormula("='Controle de Questões'!I"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,6).setFormula("='Controle de Questões'!R"+(lastrow+1));  
  sheetfiltroprovas.getRange(lastrowfilt+1,7).setFormula("='Controle de Questões'!U"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,8).setFormula("='Controle de Questões'!X"+(lastrow+1));

  sheetfiltroprovas.getRange(lastrowfilt+1,9).setFormula("='Controle de Questões'!AS"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,10).setFormula("='Controle de Questões'!AP"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,11).setFormula("='Controle de Questões'!AW"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,12).setFormula("='Controle de Questões'!BE"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,13).setFormula("='Controle de Questões'!BM"+(lastrow+1));
  sheetfiltroprovas.getRange(lastrowfilt+1,14).setFormula("='Controle de Questões'!BX"+(lastrow+1));
  
  
  for(var i = 0; i < nquest; i++){
    sheetcontrole.getRange(4,1,1,sheetcontrole.getLastColumn()).copyTo(sheetcontrole.getRange(lastrow+2+i,1,1,sheetcontrole.getLastColumn()), SpreadsheetApp.CopyPasteType.PASTE_NORMAL, false);
    let numeroformatado = ('000' + (i + 1)).slice(-3);   
    let quest = 'Q'+ numeroformatado.toString();
    var respostadaquest = "";
    var textodaquest = gabaritodaprova[i].text;
    //Logger.log("0"+gabaritodaprova[i].answer);
    if(gabaritodaprova[i].answer == "A"||gabaritodaprova[i].answer == "B"||gabaritodaprova[i].answer == "C"||gabaritodaprova[i].answer == "D"||gabaritodaprova[i].answer == "E"){
      //Logger.log("1"+gabaritodaprova[i].answer);
      respostadaquest = gabaritodaprova[i].answer;
    }else if (gabaritodaprova[i].answer == "X"){
      //Logger.log("2"+gabaritodaprova[i].answer);
      respostadaquest = "ANULADA";
    }
    sheetcontrole.getRange(lastrow+2+i,2).setValue(nomedaprova);
    sheetcontrole.getRange(lastrow+2+i,3).setValue(quest);
    sheetcontrole.getRange(lastrow+2+i,4).setValue(ano);
    sheetcontrole.getRange(lastrow+2+i,5).setValue(sheetDropdown1);
    sheetcontrole.getRange(lastrow+2+i,6).setValue(sheetDropdown2);
    if(respostadaquest){
    sheetcontrole.getRange(lastrow+2+i,7).setValue(respostadaquest+ " - PÓS");}
    var novodocs = DriveApp.getFileById("1Zf3psdUEYEVwrUlcm4wayTd6TjMkMA2YCalg9PlpUQg").makeCopy(nomedaprova+" - "+quest,DriveApp.getFolderById(iddapastadaprova));
    setPublicPermissions(novodocs.getId());
    var doc = DocumentApp.openById(novodocs.getId());
    var body = doc.getBody();
    body.replaceText("202X",ano);
    body.replaceText("XXXX",sheetDropdown1);
    body.replaceText("RXXX",sheetDropdown2);
    body.replaceText("00X",quest);
    if(respostadaquest){
      body.replaceText("G_ABCDE",respostadaquest);
    }
    if(textodaquest){
      body.replaceText("0_AOSD",textodaquest);
    }
    sheetcontrole.getRange(lastrow+2+i,8).setValue(novodocs.getUrl());


  }
  
  
   

  
  createFilterView(ss.getId(),sheetcontrole.getSheetId(),nomedaprova,sheetcontrole.getLastRow(), "#Prova: ");
  
}


function openForm() {
  var html = HtmlService.createHtmlOutputFromFile('form.html')
    .setWidth(400)
    .setHeight(300);
  SpreadsheetApp.getUi().showModalDialog(html, 'Form');
}

function fillDropdowns() {
  var pastaarquivos = DriveApp.getFolderById("1RgzkM3XVlVuCyGi0A-rFCoeD_r2W7kGq");
  console.log(pastaarquivos.getName());
  var scriptOptions = []; // Fill this array dynamically as needed
  let files = pastaarquivos.getFiles();
  while(files.hasNext()){
  scriptOptions.push(files.next().getName());
  
  }
  
  var base = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Base de Dados");
  var sheetOptions1 = base.getRange('I:I').getValues().flat().filter(function(value) {
    return value !== ''&& value !== 'Lista de Instituições';
  });
  //Logger.log(sheetOptions1);
  
  var sheetOptions2 = ['R1','R+ CIRURGIA','R+ CLÍNICA','R+ PEDIATRIA','R+ GO'];

  return {
    scriptOptions: scriptOptions,
    sheetOptions1: sheetOptions1,
    sheetOptions2: sheetOptions2
  };
}

function createFilterView(ssID, sid, nomep, lastrowdepoisdecriar, tipo) {
  var spreadsheetId = ssID; // Substitua pelo ID da sua planilha
  var sheetId = sid; // Substitua pelo ID da folha onde deseja criar a Filter View
  var colunainicio = 1;
  var colunafim = 2;
  if(tipo != "#Prova: "){
    colunainicio = 20;
    colunafim = 21;
  }

  
  var filterViews = Sheets.Spreadsheets.get(spreadsheetId).sheets.filter(sh => sh.properties.sheetId == sheetId)[0].filterViews || [];

  filterViews.forEach(function(filterView) {
    if (filterView.title === tipo + nomep) {      
      var deleteRequest = {
        "requests": [{
          "deleteFilterView": {
            "filterId": filterView.filterViewId
          }
        }]
      };
      Sheets.Spreadsheets.batchUpdate(deleteRequest, spreadsheetId);
      Logger.log('FilterView with title "' + tipo + nomep + '" deleted.');
    }
  });

  var requests = [{
    "addFilterView": {
      "filter": {
        "title": tipo + nomep,
        "range": {
          "sheetId": sheetId,
          "startRowIndex": 1,
          "endRowIndex": 1000,
          "startColumnIndex": colunainicio,
          "endColumnIndex": colunafim
        },
        "criteria": {
          "1": {
            "condition": {
              "type": "TEXT_CONTAINS",
              "values": [{
                "userEnteredValue": nomep
              }]
            }
          }
        }
      }
    }
  }];

  var resource = {
    "requests": requests
  };

  
  try {
    var response = Sheets.Spreadsheets.batchUpdate(resource, spreadsheetId);
    var filterViewId = response.replies[0].addFilterView.filter.filterViewId;
    var filterViewUrl = `https://docs.google.com/spreadsheets/d/${spreadsheetId}/edit#gid=${sheetId}&fvid=${filterViewId}`;

    
    if(tipo == "#Prova: "){
      var sp = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Filtros - Provas");
      sp.getRange(sp.getLastRow(),3).setValue(filterViewUrl);
    }else{
      Logger.log("Deu certo com o comentarista");
    }
  } catch (e) {
    Logger.log('Erro ao criar a Filter View: ' + e.message);
  }
}

function createFilterViewteste(ssID, sid, nomep, lastrowdepoisdecriar, tipo) {
  var spreadsheetId = ssID; // Substitua pelo ID da sua planilha
  var sheetId = sid; // Substitua pelo ID da folha onde deseja criar a Filter View
  var colunainicio = 1;
  var colunafim = 2;
  var requests = [];
  if(tipo != "#Prova: "){
    colunainicio = 20;
    colunafim = 21;
    requests = [{
    "addFilterView": {
      "filter": {
        "title": tipo + nomep,
        "range": {
          "sheetId": sheetId,
          "startRowIndex": 1,
          "endRowIndex": 1000,
          "startColumnIndex": colunainicio,
          "endColumnIndex": colunafim
        },
        "criteria": {
          "20": {
            "condition": {
              "type": "TEXT_CONTAINS",
              "values": [{
                "userEnteredValue": nomep
              }]
            }
          }
        }
      }
    }
  }];
    
  }else{
    requests = [{
    "addFilterView": {
      "filter": {
        "title": tipo + nomep,
        "range": {
          "sheetId": sheetId,
          "startRowIndex": 1,
          "endRowIndex": 1000,
          "startColumnIndex": colunainicio,
          "endColumnIndex": colunafim
        },
        "criteria": {
          "1": {
            "condition": {
              "type": "TEXT_CONTAINS",
              "values": [{
                "userEnteredValue": nomep
              }]
            }
          }
        }
      }
    }
  }];
  }
  

  var resource = {
    "requests": requests
  };

  
  try {
    var response = Sheets.Spreadsheets.batchUpdate(resource, spreadsheetId);
    var filterViewId = response.replies[0].addFilterView.filter.filterViewId;
    var filterViewUrl = `https://docs.google.com/spreadsheets/d/${spreadsheetId}/edit#gid=${sheetId}&fvid=${filterViewId}`;

    
    if(tipo == "#Prova: "){
      var sp = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Filtros - Provas");
      sp.getRange(sp.getLastRow(),3).setValue(filterViewUrl);
    }else{
      return(filterViewUrl);
    }
  } catch (e) {
    Logger.log('Erro ao criar a Filter View: ' + e.message);
  }
}

function filtercomentaristas(){
  var one = SpreadsheetApp.getActiveSpreadsheet().getId();
  var two = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Controle de Questões").getSheetId();
  var shetcoment = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Filtros - Comentaristas");
  var datacoment = shetcoment.getDataRange().getValues();
  for(var i = 1; i<datacoment.length;i++){
    var nomecoment = datacoment[i][0];
    
    if(nomecoment.toString() != ""){
      var url = createFilterViewteste(one,two,nomecoment,1, "#Comentarista: ");
      shetcoment.getRange(i+1,2).setValue(url);

    }
    
  }
  
}

function checarEntregaComentaristas(){
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheetcontrole = ss.getSheetByName("Controle de Questões");
  var shetgabs = ss.getSheetByName("gabs");
  var data = sheetcontrole.getDataRange().getValues();
  Logger.log(data[286][8]);
  shetgabs.clear();
  for(var i=312;i<data.length;i++){
    if(!data[i][23]&&data[i][2].toString().substring(0,1)=="Q"){
      shetgabs.getRange(i+1,1).setFormula("='Controle de Questões'!H"+(i+1)+".url");
    }
  }
  SpreadsheetApp.flush();
  puxarEntregaComentaristas();


}

function puxarEntregaComentaristas(){
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheetcontrole = ss.getSheetByName("Controle de Questões");
  var shetgabs = ss.getSheetByName("gabs");
  var data = shetgabs.getDataRange().getValues();
  for(var i=0;i<data.length;i++){
    if(data[i][0].toString().substring(0,12)=="https://docs"){
      var doc = DocumentApp.openByUrl(data[i][0]);
      Logger.log(doc.getId());
      var x = doc.getBody().getTables();
      var docum = Docs.Documents.get(doc.getId()).lists;
      var sim = x[2].getCell(0,0).getText();

      if(sim.toLowerCase() == "sim"){
        sheetcontrole.getRange(i+1,24).setValue(true);
      }
      //checkElements(docum);
    }
  }

}


function setPublicPermissions(fileId) {
  var file = DriveApp.getFileById(fileId);
  
  // Definir as permissões para "anyone with the link" e "can view"
  file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  
  Logger.log('Permissões definidas para o arquivo com ID: ' + fileId);
}