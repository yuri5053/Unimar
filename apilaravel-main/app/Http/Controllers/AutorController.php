<?php

namespace App\Http\Controllers;

use App\UseCases\AutorUseCase;
use App\Http\Requests\StoreAutorRequest;
use App\Http\Requests\UpdateAutorRequest;
use App\Http\Resources\AutorResource;

/**
 * @OA\Tag(
 *     name="Autores",
 *     description="Endpoints para gerenciar autores"
 * )
 */
class AutorController extends Controller
{
    protected $service;

    public function __construct(AutorUseCase $service)
    {
        $this->service = $service;
    }

    /**
     * @OA\Get(
     *      path="/api/autores",
     *      operationId="getAutoresList",
     *      tags={"Autores"},
     *      summary="Lista todos os autores",
     *      description="Retorna uma lista de autores",
     *      security={{"apiAuth":{}}},
     *      @OA\Response(
     *          response=200,
     *          description="Operação bem-sucedida",
     *          @OA\JsonContent(
     *              type="array",
     *              @OA\Items(ref="#/components/schemas/Autor")
     *          )
     *       ),
     *      @OA\Response(
     *          response=401,
     *          description="Não autorizado"
     *      )
     *     )
     */
    public function index()
    {
        $autores = $this->service->getAll();
        return AutorResource::collection($autores);
    }

    /**
     * @OA\Post(
     *      path="/api/autores",
     *      operationId="storeAutor",
     *      tags={"Autores"},
     *      summary="Cria um novo autor",
     *      description="Cria um novo autor e o retorna",
     *      security={{"apiAuth":{}}},
     *      @OA\RequestBody(
     *          required=true,
     *          @OA\JsonContent(
     *              required={"nome"},
     *              @OA\Property(property="nome", type="string", example="Machado de Assis")
     *          )
     *      ),
     *      @OA\Response(
     *          response=201,
     *          description="Autor criado com sucesso",
     *          @OA\JsonContent(ref="#/components/schemas/Autor")
     *      ),
     *      @OA\Response(
     *          response=422,
     *          description="Erro de validação"
     *      )
     * )
     */
    public function store(StoreAutorRequest $request)
    {
        $autor = $this->service->create($request->validated());
        return new AutorResource($autor);
    }

    /**
     * @OA\Get(
     *      path="/api/autores/{id}",
     *      operationId="getAutorById",
     *      tags={"Autores"},
     *      summary="Obtém um autor específico",
     *      description="Retorna os dados de um autor",
     *      security={{"apiAuth":{}}},
     *      @OA\Parameter(
     *          name="id",
     *          description="ID do Autor",
     *          required=true,
     *          in="path",
     *          @OA\Schema(
     *              type="integer"
     *          )
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Operação bem-sucedida",
     *          @OA\JsonContent(ref="#/components/schemas/Autor")
     *      ),
     *      @OA\Response(
     *          response=404,
     *          description="Autor não encontrado"
     *      )
     * )
     */
    public function show($id)
    {
        $autor = $this->service->find($id);
        if ($autor) {
            return new AutorResource($autor);
        }
        return response()->json(['message' => 'Autor não encontrado'], 404);
    }

    /**
     * @OA\Put(
     *      path="/api/autores/{id}",
     *      operationId="updateAutor",
     *      tags={"Autores"},
     *      summary="Atualiza um autor existente",
     *      description="Atualiza os dados de um autor e o retorna",
     *      security={{"apiAuth":{}}},
     *      @OA\Parameter(
     *          name="id",
     *          description="ID do Autor",
     *          required=true,
     *          in="path",
     *          @OA\Schema(
     *              type="integer"
     *          )
     *      ),
     *      @OA\RequestBody(
     *          required=true,
     *          @OA\JsonContent(
     *              @OA\Property(property="nome", type="string", example="Clarice Lispector")
     *          )
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Autor atualizado com sucesso",
     *          @OA\JsonContent(ref="#/components/schemas/Autor")
     *      ),
     *      @OA\Response(
     *          response=404,
     *          description="Autor não encontrado"
     *      )
     * )
     */
    public function update(UpdateAutorRequest $request, $id)
    {
        $autor = $this->service->update($id, $request->validated());
        if ($autor) {
            return new AutorResource($autor);
        }
        return response()->json(['message' => 'Autor não encontrado'], 404);
    }

    /**
     * @OA\Delete(
     *      path="/api/autores/{id}",
     *      operationId="deleteAutor",
     *      tags={"Autores"},
     *      summary="Deleta um autor",
     *      description="Deleta um autor existente",
     *      security={{"apiAuth":{}}},
     *      @OA\Parameter(
     *          name="id",
     *          description="ID do Autor",
     *          required=true,
     *          in="path",
     *          @OA\Schema(
     *              type="integer"
     *          )
     *      ),
     *      @OA\Response(
     *          response=200,
     *          description="Autor deletado com sucesso"
     *      ),
     *      @OA\Response(
     *          response=404,
     *          description="Autor não encontrado"
     *      )
     * )
     */
    public function destroy($id)
    {
        if ($this->service->delete($id)) {
            return response()->json(['message' => 'Autor deletado com sucesso']);
        }
        return response()->json(['message' => 'Autor não encontrado'], 404);
    }
}
