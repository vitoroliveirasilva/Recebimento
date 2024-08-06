// Função para voltar para a rota anterior
function goBack() {
    window.history.back();
}

// Função para copiar um item para a área de transferência 
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Texto copiado: ' + text);
    }, function(err) {
        console.error('Erro ao copiar o texto: ', err);
    });
}

// Usado em "/templates/edit/responsavel.html"
// Se o elemento "alterar_senha" for checked, então exibe os campos para digitar a nova senha
document.getElementById('alterar_senha').addEventListener('change', function () {
    var senhaFields = document.getElementById('senha_fields');
    if (this.checked) {
        senhaFields.style.display = 'block';
    } else {
        senhaFields.style.display = 'none';
    }
});