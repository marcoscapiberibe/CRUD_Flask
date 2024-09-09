<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="API_de_Cadastro_de_Empresas_0"></a>API de Cadastro de Empresas</h1>
<p class="has-line-data" data-line-start="2" data-line-end="3">Esta API RESTful foi desenvolvida para o gerenciamento de empresas, utilizando Flask, JWT para autenticação, SQLAlchemy para integração com um banco de dados relacional e Swagger para documentação dos endpoints.</p>
<h2 class="code-line" data-line-start=4 data-line-end=5 ><a id="Requisitos_4"></a>Requisitos</h2>
<ul>
<li class="has-line-data" data-line-start="6" data-line-end="7"><strong>Python 3.x</strong></li>
<li class="has-line-data" data-line-start="7" data-line-end="8"><strong>Pip</strong> (gerenciador de pacotes do Python)</li>
<li class="has-line-data" data-line-start="8" data-line-end="10"><strong>SQLite</strong></li>
</ul>
<h2 class="code-line" data-line-start=10 data-line-end=11 ><a id="Instalao_10"></a>Instalação</h2>
<ol>
<li class="has-line-data" data-line-start="12" data-line-end="18">
<p class="has-line-data" data-line-start="12" data-line-end="13"><strong>Clone o repositório</strong>:</p>
<pre><code class="has-line-data" data-line-start="14" data-line-end="17" class="language-bash">git <span class="hljs-built_in">clone</span> https://github.com/marcoscapiberibe/CRUD_Flask.git
<span class="hljs-built_in">cd</span> CRUD_Flask
</code></pre>
</li>
<li class="has-line-data" data-line-start="18" data-line-end="24">
<p class="has-line-data" data-line-start="18" data-line-end="19"><strong>Crie e ative um ambiente virtual</strong>:</p>
<pre><code class="has-line-data" data-line-start="20" data-line-end="23" class="language-bash">python3 -m venv env
<span class="hljs-built_in">source</span> env/bin/activate
</code></pre>
</li>
<li class="has-line-data" data-line-start="24" data-line-end="29">
<p class="has-line-data" data-line-start="24" data-line-end="25"><strong>Instale as dependências</strong>:</p>
<pre><code class="has-line-data" data-line-start="26" data-line-end="28" class="language-bash">pip3 install -r requirements.txt
</code></pre>
</li>
<li class="has-line-data" data-line-start="24" data-line-end="29">
<p class="has-line-data" data-line-start="24" data-line-end="25"><strong>Instale mais essas dependências</strong>:</p>
<pre><code class="has-line-data" data-line-start="26" data-line-end="28" class="language-bash">pip3 install flask flask-cors flask-migrate flask_swagger_ui marshmallow PyJWT
</code></pre>
</li>
<li class="has-line-data" data-line-start="29" data-line-end="37">
<p class="has-line-data" data-line-start="29" data-line-end="31"><strong>Configure o banco de dados</strong>:<br>
O projeto usa SQLite por padrão. Se desejar usar PostgreSQL ou MySQL, configure a variável <code>SQLALCHEMY_DATABASE_URI</code> no arquivo <code>config.py</code>.</p>
<p class="has-line-data" data-line-start="32" data-line-end="33">Para criar o banco de dados e aplicar as migrações, execute:</p>
<pre><code class="has-line-data" data-line-start="34" data-line-end="36" class="language-bash">flask db upgrade
</code></pre>
</li>
<li class="has-line-data" data-line-start="37" data-line-end="43">
<p class="has-line-data" data-line-start="37" data-line-end="39"><strong>Configure as variáveis de ambiente</strong>:<br>
Crie um arquivo <code>.env</code> com as seguintes variáveis:</p>
<pre><code class="has-line-data" data-line-start="40" data-line-end="42" class="language-bash">SECRET_KEY=<span class="hljs-string">'minha_chave_secreta'</span>
</code></pre>
</li>
<li class="has-line-data" data-line-start="43" data-line-end="50">
<p class="has-line-data" data-line-start="43" data-line-end="44"><strong>Execute a aplicação</strong>:</p>
<pre><code class="has-line-data" data-line-start="45" data-line-end="47" class="language-bash">python run.py
</code></pre>
<p class="has-line-data" data-line-start="48" data-line-end="49">A API estará disponível em <code>http://127.0.0.1:5000</code>.</p>
</li>
</ol>
<h2 class="code-line" data-line-start=50 data-line-end=51 ><a id="Endpoints_50"></a>Endpoints</h2>
<h3 class="code-line" data-line-start=52 data-line-end=53 ><a id="Autenticao_52"></a>Autenticação</h3>
<ul>
<li class="has-line-data" data-line-start="54" data-line-end="64"><strong>Login</strong>: <code>POST /login</code>
<ul>
<li class="has-line-data" data-line-start="55" data-line-end="62">Body (JSON):<pre><code class="has-line-data" data-line-start="57" data-line-end="62" class="language-json">{
  "<span class="hljs-attribute">username</span>": <span class="hljs-value"><span class="hljs-string">"admin"</span></span>,
  "<span class="hljs-attribute">password</span>": <span class="hljs-value"><span class="hljs-string">"senha654321"</span>
</span>}
</code></pre>
</li>
<li class="has-line-data" data-line-start="62" data-line-end="64">Retorna um token JWT que deve ser usado para acessar os outros endpoints.</li>
</ul>
</li>
</ul>
<h3 class="code-line" data-line-start=64 data-line-end=65 ><a id="Empresas_64"></a>Empresas</h3>
<ul>
<li class="has-line-data" data-line-start="66" data-line-end="81">
<p class="has-line-data" data-line-start="66" data-line-end="67"><strong>Criar Empresa</strong>: <code>POST /empresa</code></p>
<ul>
<li class="has-line-data" data-line-start="67" data-line-end="71">Header:<pre><code class="has-line-data" data-line-start="69" data-line-end="71">Authorization: Bearer &lt;SEU_TOKEN_JWT&gt;
</code></pre>
</li>
<li class="has-line-data" data-line-start="71" data-line-end="81">Body (JSON):<pre><code class="has-line-data" data-line-start="73" data-line-end="80" class="language-json">{
  "<span class="hljs-attribute">cnpj</span>": <span class="hljs-value"><span class="hljs-string">"00000000000100"</span></span>,
  "<span class="hljs-attribute">nome_razao</span>": <span class="hljs-value"><span class="hljs-string">"Empresa Exemplo S.A."</span></span>,
  "<span class="hljs-attribute">nome_fantasia</span>": <span class="hljs-value"><span class="hljs-string">"Exemplo"</span></span>,
  "<span class="hljs-attribute">cnae</span>": <span class="hljs-value"><span class="hljs-string">"6201502"</span>
</span>}
</code></pre>
</li>
</ul>
</li>
<li class="has-line-data" data-line-start="81" data-line-end="83">
<p class="has-line-data" data-line-start="81" data-line-end="82"><strong>Listar Empresas (com paginação)</strong>: <code>GET /empresas?start=0&amp;limit=10&amp;sort=nome_razao&amp;dir=asc</code></p>
</li>
<li class="has-line-data" data-line-start="83" data-line-end="96">
<p class="has-line-data" data-line-start="83" data-line-end="84"><strong>Atualizar Empresa</strong>: <code>PUT /empresa/&lt;cnpj&gt;</code></p>
<ul>
<li class="has-line-data" data-line-start="84" data-line-end="88">Header:<pre><code class="has-line-data" data-line-start="86" data-line-end="88">Authorization: Bearer &lt;SEU_TOKEN_JWT&gt;
</code></pre>
</li>
<li class="has-line-data" data-line-start="88" data-line-end="96">Body (JSON):<pre><code class="has-line-data" data-line-start="90" data-line-end="95" class="language-json">{
  "<span class="hljs-attribute">nome_fantasia</span>": <span class="hljs-value"><span class="hljs-string">"Novo Nome Fantasia"</span></span>,
  "<span class="hljs-attribute">cnae</span>": <span class="hljs-value"><span class="hljs-string">"6201502"</span>
</span>}
</code></pre>
</li>
</ul>
</li>
<li class="has-line-data" data-line-start="96" data-line-end="102">
<p class="has-line-data" data-line-start="96" data-line-end="97"><strong>Deletar Empresa</strong>: <code>DELETE /empresa/&lt;cnpj&gt;</code></p>
<ul>
<li class="has-line-data" data-line-start="97" data-line-end="102">Header:<pre><code class="has-line-data" data-line-start="99" data-line-end="101">Authorization: Bearer &lt;SEU_TOKEN_JWT&gt;
</code></pre>
</li>
</ul>
</li>
</ul>
<h2 class="code-line" data-line-start=102 data-line-end=103 ><a id="Documentao_Swagger_102"></a>Documentação Swagger</h2>
<p class="has-line-data" data-line-start="104" data-line-end="105">A API possui uma documentação interativa via <strong>Swagger</strong>, que permite visualizar e testar todos os endpoints diretamente no navegador.</p>
<ol>
<li class="has-line-data" data-line-start="106" data-line-end="111">
<p class="has-line-data" data-line-start="106" data-line-end="107">Após iniciar a aplicação, acesse a documentação Swagger em:</p>
<pre><code class="has-line-data" data-line-start="108" data-line-end="110">http://127.0.0.1:5000/swagger/
</code></pre>
</li>
<li class="has-line-data" data-line-start="111" data-line-end="117">
<p class="has-line-data" data-line-start="111" data-line-end="112">No Swagger, você pode testar diretamente os endpoints fornecendo o token JWT de autenticação.</p>
<ul>
<li class="has-line-data" data-line-start="113" data-line-end="114">Para testar os endpoints protegidos, faça login e copie o token JWT retornado.</li>
<li class="has-line-data" data-line-start="114" data-line-end="115">No Swagger, clique em <strong>Authorize</strong> e cole o token no formato: <code>Bearer &lt;SEU_TOKEN_JWT&gt;</code>.</li>
<li class="has-line-data" data-line-start="115" data-line-end="117">Agora você pode executar as operações CRUD diretamente pela interface do Swagger.</li>
</ul>
</li>
</ol>
<h2 class="code-line" data-line-start=117 data-line-end=118 ><a id="Testando_a_API_117"></a>Testando a API</h2>
<p class="has-line-data" data-line-start="119" data-line-end="120">Você pode testar a API usando <strong>Postman</strong>, <strong>cURL</strong>, ou a interface do <strong>Swagger</strong>.</p>
<h3 class="code-line" data-line-start=121 data-line-end=122 ><a id="Exemplo_de_cURL_para_Criar_uma_Empresa_121"></a>Exemplo de cURL para Criar uma Empresa:</h3>
<pre><code class="has-line-data" data-line-start="124" data-line-end="134" class="language-bash">curl -X POST http://<span class="hljs-number">127.0</span>.<span class="hljs-number">0.1</span>:<span class="hljs-number">5000</span>/empresa \
-H <span class="hljs-string">"Authorization: Bearer &lt;SEU_TOKEN_JWT&gt;"</span> \
-H <span class="hljs-string">"Content-Type: application/json"</span> \
<span class="hljs-operator">-d</span> <span class="hljs-string">'{
  "cnpj": "00000000000100",
  "nome_razao": "Empresa Exemplo",
  "nome_fantasia": "Exemplo",
  "cnae": "6201502"
}'</span>
</code></pre>
<h2 class="code-line" data-line-start=135 data-line-end=136 ><a id="Consideraes_Importantes_135"></a>Considerações Importantes</h2>
<ul>
<li class="has-line-data" data-line-start="137" data-line-end="138"><strong>JWT</strong>: Todos os endpoints de CRUD (criar, atualizar, deletar empresas) exigem um token JWT para autenticação.</li>
<li class="has-line-data" data-line-start="138" data-line-end="139"><strong>Documentação Swagger</strong>: A interface do Swagger facilita o teste de todos os endpoints de maneira interativa.</li>
<li class="has-line-data" data-line-start="139" data-line-end="140"><strong>Banco de Dados</strong>: Para alterar o banco de dados de SQLite para PostgreSQL ou MySQL, modifique a configuração no arquivo <code>config.py</code> e ajuste o URI de conexão de acordo com o banco de dados desejado.</li>
</ul>

