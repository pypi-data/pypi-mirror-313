-- public.criterio_capa definição
-- drop table
-- drop table criterio_capa;
create table criterio_capa (
    sq_criterio serial4 not null,
    sg_criteriopt varchar(1024) not null,
    sg_criterioen varchar(1024) not null,
    ds_criteriopt varchar(1024) not null,
    ds_criterioen varchar(1024) not null,
    ds_htmlcolor varchar(256) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint criterio_color_unique unique (ds_htmlcolor),
    constraint criterio_dsen_unique unique (sg_criterioen),
    constraint criterio_dspt_unique unique (sg_criteriopt),
    constraint criterio_pk primary key (sq_criterio),
    constraint criteriosub_sq_unidade_fk foreign key (fk_unidade) references sistema_unidade (sq_unidade)
);

-- public.empresa definição
-- drop table
-- drop table empresa;
create table empresa (
    sq_empresa serial4 not null,
    ds_empresa varchar(1024) not null,
    ds_razaosocial varchar(1024) not null,
    ds_cnpj varchar(1024) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint empresa_ds_cnpj unique (ds_cnpj),
    constraint empresa_ds_razao unique (ds_razaosocial),
    constraint empresa_ds_unique unique (ds_empresa),
    constraint empresa_pk primary key (sq_empresa)
);

-- public.perfil definição
-- drop table
-- drop table perfil;
create table perfil (
    sq_perfil serial4 not null,
    ds_perfil varchar(1024) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint perfil_ds_unique unique (ds_perfil),
    constraint perfil_pk primary key (sq_perfil)
);

-- public.permissao definição
-- drop table
-- drop table permissao;
create table permissao (
    sq_permissao serial4 not null,
    ds_permissao varchar(1024) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint permissao_ds_unique unique (ds_permissao),
    constraint permissao_pk primary key (sq_permissao)
);

-- public.pessoa definição
-- drop table
-- drop table pessoa;
create table pessoa (
    sq_pessoa serial4 not null,
    ds_name varchar(1024) not null,
    ds_socialname varchar(1024) null,
    uq_cpfcnpj varchar(255) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizacao int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    uq_email varchar null,
    constraint pessoa_cpfcnpj_unique unique (uq_cpfcnpj),
    constraint pessoa_pk primary key (sq_pessoa),
    constraint pessoa_unique unique (uq_email)
);

-- public.projeto_pessoa definição
-- drop table
-- drop table projeto_pessoa;
create table projeto_pessoa (
    sq_projetopessoa serial4 not null,
    fk_projeto int4 null,
    fk_pessoa int4 null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint projeto_pessoa_fk_unique unique (fk_projeto, fk_pessoa),
    constraint projetopessoa_pk primary key (sq_projetopessoa)
);

-- public.sistema_preferencia_tipo definição
-- drop table
-- drop table sistema_preferencia_tipo;
create table sistema_preferencia_tipo (
    sq_preferenciatipo serial4 not null,
    sg_funcao varchar(1024) not null,
    ds_funcao varchar(1024) not null,
    ds_comentario varchar(1024) not null,
    nr_funcao int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint sistema_preferenciatipo_ds_unique unique (sg_funcao),
    constraint sistema_preferenciatipo_pk primary key (sq_preferenciatipo)
);

-- public.sistema_submarino definição
-- drop table
-- drop table sistema_submarino;
create table sistema_submarino (
    sq_submarino serial4 not null,
    sg_submarino varchar(1024) not null,
    ds_submarinopt varchar(1024) not null,
    ds_submarinoen varchar(1024) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint sistemasubmarino_ds_unique unique (sg_submarino),
    constraint sistemasubmarino_pk primary key (sq_submarino)
);

-- public.sistema_tag definição
-- drop table
-- drop table sistema_tag;
create table sistema_tag (
    sq_tag serial4 not null,
    sg_tag varchar(1024) not null,
    ds_tag varchar(1024) not null,
    fk_usuario_cadastro int4 not null,
    fk_usuario_atualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint sistematag_ds_unique unique (sg_tag),
    constraint sistematag_pk primary key (sq_tag)
);

-- public.sistema_unidade definição
-- drop table
-- drop table sistema_unidade;
create table sistema_unidade (
    sq_unidade serial4 not null,
    sg_unidade varchar(1024) not null,
    ds_unidadept varchar(1024) not null,
    ds_unidadeen varchar(1024) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint sistemaunidade_ds_unique unique (sg_unidade),
    constraint sistemaunidade_pk primary key (sq_unidade)
);

-- public.criterio_sub definição
-- drop table
-- drop table criterio_sub;
create table criterio_sub (
    sq_subcriterio serial4 not null,
    sg_subcriteriopt varchar(1024) not null,
    sg_subcriterioen varchar(1024) not null,
    ds_subcriteriopt varchar(1024) not null,
    ds_subcriterioen varchar(1024) not null,
    ds_html_color varchar(256) not null,
    fk_criterio int4 not null,
    fk_unidade int4 not null,
    ds_criterio varchar(1024) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint criteriosub_color_unique unique (ds_html_color),
    constraint criteriosub_dsen_unique unique (sg_subcriterioen),
    constraint criteriosub_dspt_unique unique (sg_subcriteriopt),
    constraint criteriosub_pk primary key (sq_subcriterio),
    constraint criteriosub_sq_criterio_fk foreign key (fk_criterio) references criterio_capa (sq_criterio),
    constraint criteriosub_sq_unidade_fk foreign key (fk_unidade) references sistema_unidade (sq_unidade)
);

-- public.empresa_pessoa definição
-- drop table
-- drop table empresa_pessoa;
create table empresa_pessoa (
    sq_empresapessoa serial4 not null,
    fk_empresa int4 null,
    fk_pessoa int4 not null,
    fk_perfil int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint empresa_pessoa_pk primary key (sq_empresapessoa),
    constraint empresa_pessoa_unique unique (fk_empresa, fk_pessoa),
    constraint empresa_pessoa_sq_empresa_fk foreign key (fk_empresa) references empresa (sq_empresa),
    constraint empresa_pessoa_sq_perfl_fk foreign key (fk_perfil) references perfil (sq_perfil),
    constraint empresa_pessoa_sq_pessoa_fk foreign key (fk_pessoa) references pessoa (sq_pessoa)
);

-- public.estudocaso_tipo_modulo definição
-- drop table
-- drop table estudocaso_tipo_modulo;
create table estudocaso_tipo_modulo (
    sq_tipomodulo serial4 not null,
    sg_tipomodulo varchar(255) not null,
    ds_tipomodulo_pt varchar(1024) not null,
    ds_tipomodulo_en varchar(1024) not null,
    fk_empresa int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint estudocaso_tipo_modulo_pkey primary key (sq_tipomodulo),
    constraint estudocaso_tipo_modulo_sg_tipomodulo_key unique (sg_tipomodulo),
    constraint estudocaso_tipo_modulo_fk_empresa_fkey foreign key (fk_empresa) references empresa (sq_empresa)
);

-- public.perfil_permissao definição
-- drop table
-- drop table perfil_permissao;
create table perfil_permissao (
    sq_perfilpermissao serial4 not null,
    fk_perfil int4 not null,
    fk_permissao int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint perfil_permissao_pk primary key (sq_perfilpermissao),
    constraint perfil_permissao_unique unique (fk_perfil, fk_permissao),
    constraint perfil_permissao_sq_perfil_fk foreign key (fk_perfil) references perfil (sq_perfil),
    constraint perfil_permissao_sq_permissao_fk foreign key (fk_permissao) references permissao (sq_permissao)
);

-- public.preferencia_capa definição
-- drop table
-- drop table preferencia_capa;
create table preferencia_capa (
    sq_preferencia serial4 not null,
    fk_empresa int4 not null,
    fk_subcriterio int4 not null,
    ds_htmlcolor varchar(256) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint preferencia_color_unique unique (ds_htmlcolor),
    constraint preferencia_fk_unique unique (fk_empresa, fk_subcriterio),
    constraint preferencia_pk primary key (sq_preferencia),
    constraint preferencia_sq_empresa_fk foreign key (fk_empresa) references empresa (sq_empresa),
    constraint preferencia_sq_subcriterio_fk foreign key (fk_subcriterio) references criterio_sub (sq_subcriterio)
);

-- public.preferencia_valor definição
-- drop table
-- drop table preferencia_valor;
create table preferencia_valor (
    sq_preferenciavalor serial4 not null,
    sg_preferenciavalorpt varchar(1024) not null,
    sg_preferenciavaloren varchar(1024) not null,
    ds_preferenciavalorpt varchar(1024) not null,
    ds_preferenciavaloren varchar(1024) not null,
    b_preferenciapadrao bool not null,
    fk_preferencia int4 not null,
    fk_preferenciatipo int4 not null,
    vl_minmax int4 null,
    vl_p numeric null,
    vl_q numeric null,
    vl_s numeric null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint preferencia_valor_en_fk_unique unique (sg_preferenciavaloren, fk_preferencia),
    constraint preferencia_valor_pt_fk_unique unique (sg_preferenciavalorpt, fk_preferencia),
    constraint preferenciavalor_pk primary key (sq_preferenciavalor),
    constraint preferenciavalor_sq_preferencia_fk foreign key (fk_preferencia) references preferencia_capa (sq_preferencia),
    constraint preferenciavalor_sq_preferenciatipo_fk foreign key (fk_preferenciatipo) references sistema_preferencia_tipo (sq_preferenciatipo)
);

-- public.projeto definição
-- drop table
-- drop table projeto;
create table projeto (
    sq_projeto serial4 not null,
    sg_projetopt varchar(1024) not null,
    sg_projetoen varchar(1024) not null,
    ds_projeto varchar(1024) not null,
    ds_endereco varchar(1024) null,
    fk_empresa int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint projeto_en_fk_unique unique (sg_projetoen, fk_empresa),
    constraint projeto_pk primary key (sq_projeto),
    constraint projeto_pt_fk_unique unique (sg_projetopt, fk_empresa),
    constraint projeto_sq_empresa_fk foreign key (fk_empresa) references empresa (sq_empresa)
);

-- public.sistema_especificacao definição
-- drop table
-- drop table sistema_especificacao;
create table sistema_especificacao (
    sq_especificacao serial4 not null,
    sg_especificacao varchar(255) not null,
    ds_especificacao_pt varchar(1024) not null,
    ds_especificacao_en varchar(1024) not null,
    fk_empresa int4 not null,
    fk_unidade int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint sistema_especificacao_pkey primary key (sq_especificacao),
    constraint sistema_especificacao_sg_especificacao_key unique (sg_especificacao),
    constraint sistema_especificacao_fk_empresa_fkey foreign key (fk_empresa) references empresa (sq_empresa),
    constraint sistema_especificacao_fk_unidade_fkey foreign key (fk_unidade) references sistema_unidade (sq_unidade)
);

-- public.sistema_fabricante definição
-- drop table
-- drop table sistema_fabricante;
create table sistema_fabricante (
    sq_fabricante serial4 not null,
    sg_fabricante varchar(255) not null,
    ds_fabricante_pt varchar(1024) not null,
    ds_fabricante_en varchar(1024) not null,
    fk_empresa int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint sistema_fabricante_pkey primary key (sq_fabricante),
    constraint sistema_fabricante_sg_fabricante_key unique (sg_fabricante),
    constraint sistema_fabricante_fk_empresa_fkey foreign key (fk_empresa) references empresa (sq_empresa)
);

-- public.sistema_tipo_uso definição
-- drop table
-- drop table sistema_tipo_uso;
create table sistema_tipo_uso (
    sq_tipouso serial4 not null,
    sg_tipouso varchar(255) not null,
    ds_tipouso varchar(1024) not null,
    fk_empresa int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint sistema_tipo_uso_pkey primary key (sq_tipouso),
    constraint sistema_tipo_uso_sg_tipouso_key unique (sg_tipouso),
    constraint sistema_tipo_uso_fk_empresa_fkey foreign key (fk_empresa) references empresa (sq_empresa)
);

-- public.usuario definição
-- drop table
-- drop table usuario;
create table usuario (
    sq_usuario serial4 not null,
    fk_pessoa int4 not null,
    ds_usuario varchar(255) null,
    ds_password varchar(255) null,
    b_superuser bool default false not null,
    constraint usuario_ds_unique unique (ds_usuario),
    constraint usuario_pk primary key (sq_usuario),
    constraint usuario_pessoa_sq_pessoa_fk foreign key (fk_pessoa) references pessoa (sq_pessoa) on delete restrict
);

-- public.estudodecaso_capa definição
-- drop table
-- drop table estudodecaso_capa;
create table estudodecaso_capa (
    sq_estudo serial4 not null,
    sg_estudo varchar(1024) not null,
    ds_estudopt varchar(1024) not null,
    ds_estudoen varchar(1024) not null,
    fk_projeto int4 not null,
    fk_empresa int4 not null,
    ds_endereco varchar(1024) null,
    ds_geolocalizacao varchar(1024) not null,
    ds_status varchar(1024) not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_capa_pk primary key (sq_estudo),
    constraint estudodecaso_fk_unique unique (sg_estudo, fk_empresa),
    constraint estudodecaso_sq_empresa_fk foreign key (fk_empresa) references empresa (sq_empresa),
    constraint estudodecaso_sq_projeto_fk foreign key (fk_projeto) references projeto (sq_projeto)
);

-- public.estudodecaso_cenario definição
-- drop table
-- drop table estudodecaso_cenario;
create table estudodecaso_cenario (
    sq_estudodecasocenario serial4 not null,
    sg_cenario varchar(1024) not null,
    ds_cenariopt varchar(1024) not null,
    ds_cenarioen varchar(1024) not null,
    ds_htmlcolor varchar(256) not null,
    fk_estudo int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_cenario_fk_unique unique (fk_estudo, sg_cenario),
    constraint estudodecaso_cenario_pk primary key (sq_estudodecasocenario),
    constraint estudodecaso_color_unique unique (fk_estudo, ds_htmlcolor),
    constraint estudodecaso_cenario_sq_estudo_fk foreign key (fk_estudo) references estudodecaso_capa (sq_estudo)
);

-- public.estudodecaso_grupo definição
-- drop table
-- drop table estudodecaso_grupo;
create table estudodecaso_grupo (
    sq_estudodecasogrupo serial4 not null,
    sg_grupo varchar(1024) not null,
    ds_grupopt varchar(1024) not null,
    ds_grupoen varchar(1024) not null,
    fk_estudo int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_grupo_fk_unique unique (fk_estudo, sg_grupo),
    constraint estudodecaso_grupo_pk primary key (sq_estudodecasogrupo),
    constraint estudodecaso_gruposq_estudo_fk foreign key (fk_estudo) references estudodecaso_capa (sq_estudo)
);

-- public.estudodecaso_pessoa definição
-- drop table
-- drop table estudodecaso_pessoa;
create table estudodecaso_pessoa (
    sq_estudodecasopessoa serial4 not null,
    fk_estudo int4 not null,
    fk_pessoa int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_pessoa_fk_unique unique (fk_estudo, fk_pessoa),
    constraint estudodecaso_pessoa_pk primary key (sq_estudodecasopessoa),
    constraint estudodecaso_pessoa_sq_estudo_fk foreign key (fk_estudo) references estudodecaso_capa (sq_estudo),
    constraint estudodecaso_pessoa_sq_pessoa_fk foreign key (fk_pessoa) references pessoa (sq_pessoa)
);

-- public.estudodecaso_subcriterio definição
-- drop table
-- drop table estudodecaso_subcriterio;
create table estudodecaso_subcriterio (
    sq_estudodecasosubcriterio serial4 not null,
    fk_estudo int4 not null,
    fk_subcriterio int4 not null,
    fk_preferenciavalor int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_subcriterio_fk_unique unique (fk_estudo, fk_subcriterio),
    constraint estudodecaso_subcriterio_pk primary key (sq_estudodecasosubcriterio),
    constraint estudodecaso_subcriterio_sq_estudo_fk foreign key (fk_estudo) references estudodecaso_capa (sq_estudo),
    constraint estudodecaso_subcriterio_sq_preferenciavalor_fk foreign key (fk_preferenciavalor) references preferencia_valor (sq_preferenciavalor),
    constraint estudodecaso_subcriterio_sq_subcriterio_fk foreign key (fk_subcriterio) references criterio_sub (sq_subcriterio)
);

-- public.estudodecaso_submarino definição
-- drop table
-- drop table estudodecaso_submarino;
create table estudodecaso_submarino (
    sq_estudodecasosubmarino serial4 not null,
    fk_estudo int4 not null,
    fk_submarino int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_submarino_fk_unique unique (fk_estudo, fk_submarino),
    constraint estudodecaso_submarino_pk primary key (sq_estudodecasosubmarino),
    constraint estudodecaso_submarino_sq_estudo_fk foreign key (fk_estudo) references estudodecaso_capa (sq_estudo),
    constraint estudodecaso_submarino_sq_submarino_fk foreign key (fk_submarino) references sistema_submarino (sq_submarino)
);

-- public.estudodecaso_tag definição
-- drop table
-- drop table estudodecaso_tag;
create table estudodecaso_tag (
    sq_estudodecasotag serial4 not null,
    fk_estudo int4 not null,
    fk_tag int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_tag_fk_unique unique (fk_estudo, fk_tag),
    constraint estudodecaso_tag_pk primary key (sq_estudodecasotag),
    constraint estudodecaso_tag_sq_estudo_fk foreign key (fk_estudo) references estudodecaso_capa (sq_estudo),
    constraint estudodecaso_tag_sq_tag_fk foreign key (fk_tag) references sistema_tag (sq_tag)
);

-- public.sistema_camada definição
-- drop table
-- drop table sistema_camada;
create table sistema_camada (
    sq_duto_camada serial4 not null,
    sg_duto_camada varchar(255) not null,
    ds_duto_camada_pt varchar(1024) not null,
    ds_duto_camada_en varchar(1024) not null,
    fk_empresa int4 not null,
    fk_fabricante int4 not null,
    fk_tipouso int4 not null,
    nr_diametro numeric null,
    b_flexivel bool not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint sistema_camada_pkey primary key (sq_duto_camada),
    constraint sistema_camada_sg_duto_camada_key unique (sg_duto_camada),
    constraint sistema_camada_fk_empresa_fkey foreign key (fk_empresa) references empresa (sq_empresa),
    constraint sistema_camada_fk_fabricante_fkey foreign key (fk_fabricante) references sistema_fabricante (sq_fabricante),
    constraint sistema_camada_fk_tipouso_fkey foreign key (fk_tipouso) references sistema_tipo_uso (sq_tipouso)
);

-- public.sistema_duto definição
-- drop table
-- drop table sistema_duto;
create table sistema_duto (
    sq_duto serial4 not null,
    sg_duto varchar(255) not null,
    ds_duto_pt varchar(1024) not null,
    ds_duto_en varchar(1024) not null,
    fk_empresa int4 not null,
    fk_fabricante int4 not null,
    fk_tipouso int4 not null,
    nr_diametro numeric null,
    b_flexivel bool null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint sistema_duto_pkey primary key (sq_duto),
    constraint sistema_duto_sg_duto_key unique (sg_duto),
    constraint sistema_duto_fk_empresa_fkey foreign key (fk_empresa) references empresa (sq_empresa),
    constraint sistema_duto_fk_fabricante_fkey foreign key (fk_fabricante) references sistema_fabricante (sq_fabricante),
    constraint sistema_duto_fk_tipouso_fkey foreign key (fk_tipouso) references sistema_tipo_uso (sq_tipouso)
);

-- public.sistema_duto_especificacao definição
-- drop table
-- drop table sistema_duto_especificacao;
create table sistema_duto_especificacao (
    sq_duto_especificaao serial4 not null,
    fk_duto int4 not null,
    fk_especificacao int4 not null,
    ds_valor varchar(1024) not null,
    nr_valor numeric null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint sistema_duto_especificacao_pkey primary key (sq_duto_especificaao),
    constraint sistema_duto_especificacao_fk_duto_fkey foreign key (fk_duto) references sistema_duto (sq_duto),
    constraint sistema_duto_especificacao_fk_especificacao_fkey foreign key (fk_especificacao) references sistema_especificacao (sq_especificacao)
);

-- public.estudocaso_equipamento definição
-- drop table
-- drop table estudocaso_equipamento;
create table estudocaso_equipamento (
    sq_equipamento serial4 not null,
    sg_equipamento varchar(255) not null,
    ds_equipamento_pt varchar(1024) null,
    ds_equipamento_en varchar(1024) null,
    fk_estudo int4 not null,
    fk_modulo int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint estudocaso_equipamento_pkey primary key (sq_equipamento),
    constraint estudocaso_equipamento_sg_equipamento_key unique (sg_equipamento),
    constraint estudocaso_equipamento_fk_estudo_fkey foreign key (fk_estudo) references estudodecaso_capa (sq_estudo)
);

-- public.estudocaso_linha definição
-- drop table
-- drop table estudocaso_linha;
create table estudocaso_linha (
    sq_linha serial4 not null,
    sg_linha varchar(255) not null,
    ds_linha_pt varchar(1024) not null,
    ds_linha_en varchar(1024) not null,
    fk_estudo int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint estudocaso_linha_pkey primary key (sq_linha),
    constraint estudocaso_linha_sg_linha_key unique (sg_linha),
    constraint estudocaso_linha_fk_estudo_fkey foreign key (fk_estudo) references estudodecaso_capa (sq_estudo)
);

-- public.estudocaso_modulo definição
-- drop table
-- drop table estudocaso_modulo;
create table estudocaso_modulo (
    sq_modulo serial4 not null,
    sg_modulo varchar(255) not null,
    ds_modulo_pt varchar(1024) not null,
    ds_modulo_en varchar(1024) not null,
    fk_equipamento int4 not null,
    fk_tipomodulo int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint estudocaso_modulo_pkey primary key (sq_modulo),
    constraint estudocaso_modulo_sg_modulo_key unique (sg_modulo),
    constraint estudocaso_modulo_fk_equipamento_fkey foreign key (fk_equipamento) references estudocaso_equipamento (sq_equipamento),
    constraint estudocaso_modulo_fk_tipomodulo_fkey foreign key (fk_tipomodulo) references estudocaso_tipo_modulo (sq_tipomodulo)
);

-- public.estudocaso_zona definição
-- drop table
-- drop table estudocaso_zona;
create table estudocaso_zona (
    sq_zona serial4 not null,
    sg_zona varchar(255) not null,
    ds_zona_pt varchar(1024) not null,
    ds_zona_en varchar(1024) not null,
    fk_estudo int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint estudocaso_zona_pkey primary key (sq_zona),
    constraint estudocaso_zona_sg_zona_key unique (sg_zona),
    constraint estudocaso_zona_fk_estudo_fkey foreign key (fk_estudo) references estudodecaso_capa (sq_estudo)
);

-- public.estudodecaso_alternativa definição
-- drop table
-- drop table estudodecaso_alternativa;
create table estudodecaso_alternativa (
    sq_estudodecasoalternativa serial4 not null,
    sg_alternativa varchar(1024) not null,
    ds_alternativapt varchar(1024) not null,
    ds_alternativaen varchar(1024) not null,
    fk_estudo int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_alternativa_fk_unique unique (fk_estudo, sg_alternativa),
    constraint estudodecaso_alternativa_pk primary key (sq_estudodecasoalternativa),
    constraint estudodecaso_alternativa_sq_estudo_fk foreign key (fk_estudo) references estudodecaso_capa (sq_estudo)
);

-- public.estudodecaso_cenariopeso definição
-- drop table
-- drop table estudodecaso_cenariopeso;
create table estudodecaso_cenariopeso (
    sq_estudodecasopeso serial4 not null,
    vl_peso numeric null,
    fk_cenario int4 not null,
    fk_subcriterio int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_peso_fk_unique unique (fk_cenario, fk_subcriterio),
    constraint estudodecaso_peso_pk primary key (sq_estudodecasopeso),
    constraint estudodecaso_peso_sq_cenario_fk foreign key (fk_cenario) references estudodecaso_cenario (sq_estudodecasocenario),
    constraint estudodecaso_peso_sq_subcriterio_fk foreign key (fk_subcriterio) references estudodecaso_subcriterio (sq_estudodecasosubcriterio)
);

-- public.estudodecaso_grupo_alternativa definição
-- drop table
-- drop table estudodecaso_grupo_alternativa;
create table estudodecaso_grupo_alternativa (
    sq_estudodecasogrupoalternativa int4 not null,
    fk_alternativa int4 not null,
    fk_grupo int4 not null,
    b_selecao bool not null,
    fk_usuarioselecao int4 not null,
    dt_selecao timestamp not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_grupoalternativa_fk_unique unique (fk_alternativa, fk_grupo),
    constraint estudodecaso_grupoalternativa_pk primary key (sq_estudodecasogrupoalternativa),
    constraint estudodecaso_grupoalternativa_sq_grupo_fk foreign key (fk_grupo) references estudodecaso_grupo (sq_estudodecasogrupo),
    constraint estudodecaso_grupotalternativa_sq_alternativa_fk foreign key (fk_alternativa) references estudodecaso_alternativa (sq_estudodecasoalternativa)
);

-- public.estudodecaso_notatecnica definição
-- drop table
-- drop table estudodecaso_notatecnica;
create table estudodecaso_notatecnica (
    sq_estudodecasonotatecnica serial4 not null,
    vl_notatecnica numeric not null,
    fk_grupoalternativa int4 not null,
    fk_estudodecasosubcriterio int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp not null,
    b_ativo bool default true not null,
    constraint estudodecaso_notatecnica_fk_unique unique (fk_grupoalternativa, fk_estudodecasosubcriterio),
    constraint estudodecaso_notatecnica_pk primary key (sq_estudodecasonotatecnica),
    constraint estudodecaso_notatecnica_sq_grupoalternativa_fk foreign key (fk_grupoalternativa) references estudodecaso_grupo_alternativa (sq_estudodecasogrupoalternativa),
    constraint estudodecaso_notatecnica_sq_subcriterio_fk foreign key (fk_estudodecasosubcriterio) references estudodecaso_subcriterio (sq_estudodecasosubcriterio)
);

-- public.sistema_camada_especificacao definição
-- drop table
-- drop table sistema_camada_especificacao;
create table sistema_camada_especificacao (
    sq_camada_especificacao serial4 not null,
    fk_duto int4 not null,
    fk_especificacao int4 not null,
    ds_valor varchar(1024) not null,
    nr_valor numeric null,
    fk_sistema_duto_camada int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint sistema_camada_especificacao_pkey primary key (sq_camada_especificacao),
    constraint sistema_camada_especificacao_fk_duto_fkey foreign key (fk_duto) references sistema_duto (sq_duto),
    constraint sistema_camada_especificacao_fk_especificacao_fkey foreign key (fk_especificacao) references sistema_especificacao (sq_especificacao),
    constraint sistema_camada_especificacao_fk_sistema_duto_camada_fkey foreign key (fk_sistema_duto_camada) references sistema_camada (sq_duto_camada)
);

-- public.equipamento_modulo_especificacao definição
-- drop table
-- drop table equipamento_modulo_especificacao;
create table equipamento_modulo_especificacao (
    sq_modulo_especificacao serial4 not null,
    ds_valor varchar(1024) not null,
    nr_valor numeric null,
    fk_modulo int4 not null,
    fk_especificacao int4 not null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint equipamento_modulo_especificacao_pkey primary key (sq_modulo_especificacao),
    constraint equipamento_modulo_especificacao_fk_especificacao_fkey foreign key (fk_especificacao) references sistema_especificacao (sq_especificacao),
    constraint equipamento_modulo_especificacao_fk_modulo_fkey foreign key (fk_modulo) references estudocaso_modulo (sq_modulo)
);

-- public.estudocaso_tramo definição
-- drop table
-- drop table estudocaso_tramo;
create table estudocaso_tramo (
    sq_tramo serial4 not null,
    sg_tramo varchar(255) not null,
    ds_tramo_pt varchar(1024) not null,
    ds_tramo_en varchar(1024) not null,
    fk_linha int4 not null,
    fk_duto int4 not null,
    fk_zona int4 not null,
    nr_profundidade numeric null,
    nr_comprimento numeric null,
    nr_comprimentocoral numeric null,
    nr_corte numeric null,
    nr_anodo numeric null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint estudocaso_tramo_pkey primary key (sq_tramo),
    constraint estudocaso_tramo_sg_tramo_key unique (sg_tramo),
    constraint estudocaso_tramo_fk_duto_fkey foreign key (fk_duto) references sistema_duto (sq_duto),
    constraint estudocaso_tramo_fk_linha_fkey foreign key (fk_linha) references estudocaso_linha (sq_linha),
    constraint estudocaso_tramo_fk_zona_fkey foreign key (fk_zona) references estudocaso_zona (sq_zona)
);

-- public.estudocaso_produto definição
-- drop table
-- drop table estudocaso_produto;
create table estudocaso_produto (
    sq_produto serial4 not null,
    fk_estudo int4 not null,
    fk_grupo int4 not null,
    fk_tramo int4 null,
    fk_modulo int4 null,
    fk_usuariocadastro int4 not null,
    fk_usuarioatualizado int4 not null,
    dt_cadastro timestamp not null,
    dt_atualizacao timestamp null,
    b_ativo bool default true not null,
    constraint estudocaso_produto_pkey primary key (sq_produto),
    constraint estudocaso_produto_fk_estudo_fkey foreign key (fk_estudo) references estudodecaso_capa (sq_estudo),
    constraint estudocaso_produto_fk_grupo_fkey foreign key (fk_grupo) references estudodecaso_grupo (sq_estudodecasogrupo),
    constraint estudocaso_produto_fk_modulo_fkey foreign key (fk_modulo) references estudocaso_modulo (sq_modulo),
    constraint estudocaso_produto_fk_tramo_fkey foreign key (fk_tramo) references estudocaso_tramo (sq_tramo)
);
