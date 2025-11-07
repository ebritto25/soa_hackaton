"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import ReactJson from "react18-json-view";

export default function Home() {
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const [nomeDoenca, setNomeDoenca] = useState<string | null>(null);
  const [cultura, setCultura] = useState<string | null>(null);
  const [confiabilidade, setConfiabilidade] = useState<number | null>(null);
  const [commonName, setCommonName] = useState<string | null>(null);
  const [descDoenca, setDescDoenca] = useState<string | null>(null);
  const [tratamentos, setTratamentos] = useState<any[]>([]);
  const [tratamentoIndex, setTratamentoIndex] = useState(0);

  // 📸 Função para carregar imagem
  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "image/jpeg") {
      setSelectedImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setNomeDoenca(null);
      setConfiabilidade(null);
      setCultura(null);
      setCommonName(null);
      setDescDoenca(null);
      setTratamentos([]);
      setTratamentoIndex(0);
    } else {
      alert("Por favor, selecione uma imagem JPG.");
    }
  };

  // 🔍 Função principal de diagnóstico e tratamento
  const handleSearchDisease = async () => {
    let alerta = "Erro ao processar a imagem!";

    if (!selectedImage) {
      alert("Carregue uma imagem primeiro!");
      return;
    }

    setLoading(true);
    setResult(null);
    setNomeDoenca(null);
    setConfiabilidade(null);
    setCultura(null);
    setCommonName(null);
    setDescDoenca(null);
    setTratamentos([]);
    setTratamentoIndex(0);

    try {
      const formData = new FormData();
      formData.append("file", selectedImage);

      // 1️⃣ Envia imagem para API de diagnóstico
      const response = await fetch(
        "https://leonardo-cerce-agrolens.hf.space/imageDiagnosis",
        {
          method: "POST",
          headers: { accept: "application/json" },
          body: formData,
        }
      );

      const data = await response.json();

      if (response.ok) {
        alerta = "Análise concluída.";
        if (data.scientificName == "Saudável") alerta = "Planta está saudável.";
      } else {
        alerta = response.statusText;
      }

      setResult(data.resultado || alerta);
      setNomeDoenca(data.scientificName || "—");
      setCultura(data.crop || "—");
      setConfiabilidade(data.confidence || "—");
      setCommonName(data.commonName || "—");
      setDescDoenca(data.description || "—");

      // 2️⃣ Se scientificName é válido → buscar tratamento
      if (
        data.scientificName &&
        data.scientificName.trim() !== "" &&
        data.scientificName !== "-" &&
        data.scientificName !== "Saudável"
      ) {
        const encodedName = encodeURIComponent(data.scientificName);
        const treatmentUrl = `https://leonardo-cerce-agrolens.hf.space/treatment?diseaseName=${encodedName}`;

        const treatmentResponse = await fetch(treatmentUrl, {
          method: "GET",
          headers: { accept: "application/json" },
        });

        if (!treatmentResponse.ok) {
          alert("Erro ao buscar tratamento!");
        }

        const treatmentData = await treatmentResponse.json();
        console.log("Tratamento:", treatmentData);

        // Caso venha apenas um objeto, transforma em array
        const lista = Array.isArray(treatmentData)
          ? treatmentData
          : [treatmentData];

        setTratamentos(lista);
        setTratamentoIndex(0);
      } else {
        setTratamentos([]);
      }
    } catch (error) {
      console.error(error);
      setResult({ erro: "Falha ao processar imagem ou obter tratamento." });
    } finally {
      setLoading(false);
    }
  };

  // Função auxiliar: detectar JSONs grandes
  const isLargeJson = (data: any): boolean => {
    try {
      return JSON.stringify(data).length > 2000;
    } catch {
      return false;
    }
  };

  const tratamentoAtual =
    tratamentos.length > 0 ? tratamentos[tratamentoIndex] : null;

  const handleNext = () => {
    if (tratamentoIndex < tratamentos.length - 1)
      setTratamentoIndex(tratamentoIndex + 1);
  };

  const handlePrev = () => {
    if (tratamentoIndex > 0) setTratamentoIndex(tratamentoIndex - 1);
  };

  const {
    marca_comercial,
    numero_registro,
    url_agrofit,
    ...descricaotratamento
  } = tratamentoAtual || {};

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-gradient-to-b from-blue-50 to-blue-100">
      <motion.div
        className="bg-white shadow-xl rounded-2xl p-6 w-full max-w-2xl text-center"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <img
          src="logo-Agrolens2.jpg"
          alt="Logo AgroLens"
          className="mx-auto mb-4"
        />
        <h1 className="text-2xl font-bold mb-6 text-gray-700">
          🌿 Reconhecimento de Doenças de Plantas
        </h1>

        {/* Upload de imagem */}
        <input
          type="file"
          accept="image/jpeg"
          onChange={handleImageUpload}
          className="hidden"
          id="upload"
        />
        <label
          htmlFor="upload"
          className="cursor-pointer bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl shadow-md transition duration-300 inline-block"
        >
          {selectedImage ? "Carregar Nova Imagem" : "Carregar Imagem JPG"}
        </label>

        {/* Pré-visualização */}
        <AnimatePresence>
          {preview && (
            <motion.div
              key="preview"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="mt-4"
            >
              <img
                src={preview}
                alt="Pré-visualização"
                className="w-full rounded-xl border mt-2 shadow-sm"
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Botão principal */}
        <button
          onClick={handleSearchDisease}
          disabled={!selectedImage || loading}
          className={`mt-6 px-4 py-2 rounded-xl shadow-md w-full transition duration-300 flex items-center justify-center gap-2
            ${
              !selectedImage || loading
                ? "bg-gray-300 cursor-not-allowed"
                : "bg-green-500 hover:bg-green-600 text-white"
            }`}
        >
          {loading ? (
            <>
              <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
              <span>Analisando imagem...</span>
            </>
          ) : (
            "Pesquisar Doença"
          )}
        </button>

        {/* Resultado principal */}
        <AnimatePresence>
          {result && (
            <motion.div
              key="resultado"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
              className="text-2xl font-bold py-6 text-gray-700"
            >
              {result}
            </motion.div>
          )}
        </AnimatePresence>

        {/* 🧠 Identificação da Doença */}
        {nomeDoenca && cultura && commonName && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mt-3 bg-gradient-to-r from-blue-100 to-indigo-50 border border-blue-200 rounded-xl p-3 text-left"
          >
            <div className="flex items-center space-x-2">
              <h2 className="text-xl text-gray-500">Nome da cultura:</h2>
              <p className="text-lg font-semibold text-blue-700">{cultura}</p>
            </div>

            <div className="flex items-center space-x-2">
              <h2 className="text-xl text-gray-500">Nome da doença:</h2>
              <p className="text-lg font-semibold text-blue-700">
                {nomeDoenca}
              </p>
            </div>

            <div className="flex items-center space-x-2">
              <h2 className="text-xl text-gray-500">Nome comum da doença:</h2>
              <p className="text-lg font-semibold text-blue-700">
                {commonName}
              </p>
            </div>
          </motion.div>
        )}

        {/* 💊 DescDoenca sugerido */}
        {descDoenca && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="mt-3 bg-gradient-to-r from-green-100 to-indigo-50  border border-green-200 rounded-xl p-3 text-left"
          >
            <h2 className="text-xl text-gray-500">Descrição da doença:</h2>
            <p className="text-lg font-medium text-green-700">{descDoenca}</p>
          </motion.div>
        )}

        {/* 🧠 Confiabilidade */}
        {confiabilidade && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mt-3 bg-gradient-to-r from-green-100 to-blue-100 border border-blue-200 rounded-xl p-3 text-left"
          >
            <h2 className="text-xl text-center text-black font-semibold">
              Confiabilidade do modelo: {(confiabilidade*100).toFixed(4)} %
            </h2>
          </motion.div>
        )}

        {/* Tratamento */}
        {tratamentoAtual && (
          <motion.div
            key={`tratamento-${tratamentoIndex}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
            className="text-left mt-6"
          >
            {/* Header com informações do tratamento */}
            <div className="bg-gradient-to-r from-orange-100 to-indigo-50 rounded-lg p-4 mb-4 border border-blue-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xl text-gray-600">
                    Tratamento com marca comercial:
                  </p>
                  <a
                    href={tratamentoAtual.url_agrofit}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xl font-bold text-blue-600 hover:underline hover:text-blue-800"
                  >
                    🔗{tratamentoAtual.marca_comercial}
                  </a>
                </div>
                <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                  {tratamentoIndex + 1}/{tratamentos.length}
                </div>
              </div>
            </div>

            {/* Container do JSON com melhor visual */}
            <div className="border border-gray-200 rounded-xl overflow-hidden bg-white shadow-sm">
              <div className="bg-gray-50 px-4 py-2 border-b border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 flex items-center">
                  <svg
                    className="w-4 h-4 mr-2"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                    />
                  </svg>
                  Dados do Tratamento
                </h3>
              </div>
              <div className="max-h-[50vh] overflow-y-auto p-4">
                <ReactJson
                  src={descricaotratamento}
                  theme="atom"
                  collapsed={1}
                  enableClipboard={false}
                  style={{ fontSize: "14px" }}
                />
              </div>
            </div>

            {/* Navegação melhorada */}
            <div className="flex justify-between items-center mt-6 px-2">
              <button
                onClick={handlePrev}
                disabled={tratamentoIndex === 0}
                className={`flex items-center px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                  tratamentoIndex === 0
                    ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                    : "bg-blue-500 text-white hover:bg-blue-600 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
                }`}
              >
                <svg
                  className="w-4 h-4 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
                Voltar
              </button>

              {/* Indicador de progresso */}
              <div className="flex-1 max-w-xs mx-4">
                <div className="bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                    style={{
                      width: `${
                        ((tratamentoIndex + 1) / tratamentos.length) * 100
                      }%`,
                    }}
                  ></div>
                </div>
              </div>

              <button
                onClick={handleNext}
                disabled={tratamentoIndex === tratamentos.length - 1}
                className={`flex items-center px-6 py-3 rounded-xl font-medium transition-all duration-200 ${
                  tratamentoIndex === tratamentos.length - 1
                    ? "bg-gray-100 text-gray-400 cursor-not-allowed"
                    : "bg-blue-500 text-white hover:bg-blue-600 shadow-sm hover:shadow-md transform hover:-translate-y-0.5"
                }`}
              >
                Avançar
                <svg
                  className="w-4 h-4 ml-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </button>
            </div>
          </motion.div>
        )}
      </motion.div>

      <footer className="mt-6 text-sm text-gray-500">
        © 2025 AgroLensLabs – Todos os direitos reservados.
      </footer>
    </div>
  );
}
