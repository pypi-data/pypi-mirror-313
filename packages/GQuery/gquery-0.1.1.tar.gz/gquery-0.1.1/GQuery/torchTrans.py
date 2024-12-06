import torch
from torch.nn import init
from torch.nn.parameter import Parameter
from torch.nn.modules.linear import NonDynamicallyQuantizableLinear
from torch.nn.init import xavier_normal_, constant_
torch.set_default_tensor_type
import numpy as np
from time import time
#channel_last = False
import random
def makeDropout(dropout):
    if dropout>0:
        return torch.nn.Dropout(dropout)
    else:
        return torch.nn.Identity()

class FeedForward(torch.nn.Module):
    def __init__(self, d_model=512, dim_feedforward=2048, dropout=0.1, beta=1.0):
        super(FeedForward, self).__init__()
        self.linear1 = torch.nn.Linear(d_model, dim_feedforward)
        self.dropout = makeDropout(dropout)
        self.linear2 = torch.nn.Linear(dim_feedforward, d_model)
        self.beta = beta
        self.initialize()
    def initialize(self):
        init.xavier_uniform_(self.linear1.weight, gain=self.beta)
        init.xavier_uniform_(self.linear2.weight, gain=self.beta)
    def forward(self, x):
        x = self.linear1(x)
        x = torch.nn.functional.relu(x)
        x = self.dropout(x)
        x = self.linear2(x)
        return x


class Embeddings:
    def __init__(self,input_channels=10,typeList = [],typeD = {},mulA = {},paraD = {}): 
        self.input_channels = input_channels#np.sum(data.shape[-1]for data in args[::2]) 
        self.typeList = typeList
        self.typeD = typeD
        self.mulA = mulA
        self.paraD = paraD
    def __call__(self,*args,maskRatio=0.0,mask0 = [],mustTypeL=['c','water_thickness'],typeL =['c','g','rf','e','rfs','vdss','water_thickness','sediment_thickness','crust_thickness'],KL = [1,2,2,3,3,3,4,4,4,5,5,5,5,6,6,6,6,7,7,8,8,9,9]):
        
        N = self.input_channels
        
        iL =  np.arange(len(args)//3).tolist()
        
        DataL=[]
        TypeIndexL = []
        MaskL =[]
        for j in range(args[0].shape[0]):
            dataL = []
            typeIndexL = []
            #posL = []
            #CI = 0
            maskL=[]
            if maskRatio>0.0000001:
                K =  random.choice(KL)
                usedTypeL = random.sample(typeL,K)+mustTypeL
                if 'c' not in usedTypeL and 'g' not in usedTypeL and 'e' not in usedTypeL and 'rf' not in usedTypeL:
                    usedTypeL.append(random.choice(['c','g','e','rf']))
            for i in iL:
                #CI = 0
                
                data = args[3*i][j]
                para = args[3*i+1][j]
                
                typeName = args[3*i+2]
                baseName = self.typeD[typeName]
                typeNameIndex = self.typeList.index(typeName)
                baseNameIndex = self.typeList.index(baseName)
                
                paraL = self.paraD[typeName]
                paraLIndex = [self.typeList.index(para) for para in paraL]
                
                
                dataNew = np.zeros((data.shape[0],N))
                typeIndexNew = np.zeros((data.shape[0],N)).astype('int')
                dataNew[:,0] = 1
                typeIndexNew[:,0] = typeNameIndex
                dataNew[:,1] = data[:,0]/self.mulA[baseName]
                typeIndexNew[:,1] = baseNameIndex
                for k in range(min(len(paraL),para.shape[-1])):
                    dataNew[:,k+2] = para[:,k]/self.mulA[paraL[k]]
                    typeIndexNew[:,k+2] = paraLIndex[k]
                mask = 1+np.zeros((data.shape[0]))
                mask = np.where(np.isnan(dataNew).sum(axis=1)>0,0,mask)
                dataNew = np.where(np.isnan(dataNew),0,dataNew)
                dataL.append(dataNew)
                typeIndexL.append(typeIndexNew)
                if maskRatio>0.0000001:
                    if args[3*i+2] in usedTypeL:
                        if args[3*i+2] in ['c','g','e','rf','vs']:
                            mask = np.where(np.random.rand(mask.shape[0])>maskRatio,mask,0)
                        else:
                            mask[:] = 1
                    else:
                        mask[:] = 0
                mask = np.where(np.isnan(data).sum(axis=1)>0,0,mask)
                maskL.append(mask)
            data = np.concatenate(dataL,axis=0)
            typeIndex = np.concatenate(typeIndexL,axis=0)
            mask = np.concatenate(maskL)[:,np.newaxis]
            DataL.append(data)
            TypeIndexL.append(typeIndex)
            MaskL.append(mask)
        if len(mask0)>0:
            MaskL=mask0
        return np.array(DataL),np.array(TypeIndexL),np.array(MaskL)

class MultiHeadAttention_(torch.nn.MultiheadAttention):
    def __init__(self, embed_dim, num_heads, dropout=0., bias=True, add_bias_kv=False, add_zero_attn=False,
                 kdim=None, vdim=None, batch_first=False, device=None, dtype=None,beta=1):
       
        self.beta = beta
        
        if embed_dim <= 0 or num_heads <= 0:
            raise ValueError(
                f"embed_dim and num_heads must be greater than 0,"
                f" got embed_dim={embed_dim} and num_heads={num_heads} instead"
            )
        factory_kwargs = {'device': device, 'dtype': dtype}
        torch.nn.Module.__init__(self)
        self.embed_dim = embed_dim
        self.kdim = kdim if kdim is not None else embed_dim
        self.vdim = vdim if vdim is not None else embed_dim
        self._qkv_same_embed_dim = False#self.kdim == embed_dim and self.vdim == embed_dim

        self.num_heads = num_heads
        self.dropout = dropout
        self.batch_first = batch_first
        self.head_dim = embed_dim // num_heads
        assert self.head_dim * num_heads == self.embed_dim, "embed_dim must be divisible by num_heads"

        #if not self._qkv_same_embed_dim:
        self.q_proj_weight = Parameter(torch.empty((embed_dim, embed_dim), **factory_kwargs))
        self.k_proj_weight = Parameter(torch.empty((embed_dim, self.kdim), **factory_kwargs))
        self.v_proj_weight = Parameter(torch.empty((embed_dim, self.vdim), **factory_kwargs))
        self.register_parameter('in_proj_weight', None)
    

        if bias:
            self.in_proj_bias = Parameter(torch.empty(3 * embed_dim, **factory_kwargs))
        else:
            self.register_parameter('in_proj_bias', None)
        self.out_proj = NonDynamicallyQuantizableLinear(embed_dim, embed_dim, bias=bias, **factory_kwargs)

        if add_bias_kv:
            self.bias_k = Parameter(torch.empty((1, 1, embed_dim), **factory_kwargs))
            self.bias_v = Parameter(torch.empty((1, 1, embed_dim), **factory_kwargs))
        else:
            self.bias_k = self.bias_v = None

        self.add_zero_attn = add_zero_attn

        #self._reset_parameters()
        self.initialize()
    def initialize(self):
        
        
        
        if self.in_proj_bias is not None:
            constant_(self.in_proj_bias, 0.)
            constant_(self.out_proj.bias, 0.)
        if self.bias_k is not None:
            xavier_normal_(self.bias_k)
        if self.bias_v is not None:
            xavier_normal_(self.bias_v)
        torch.nn.init.xavier_uniform_(self.v_proj_weight, gain=self.beta)
        torch.nn.init.xavier_uniform_(self.out_proj.weight, gain=self.beta)
        torch.nn.init.xavier_uniform_(self.q_proj_weight, gain=1)
        torch.nn.init.xavier_uniform_(self.k_proj_weight, gain=1)
    
        

class AttentionBlock(torch.nn.Module):
    def __init__(self, d_model=512, nhead=8, dropout=0.1, beta=1.0,alpha=0.1,need_weights=False):
        super(AttentionBlock, self).__init__()
        #self.multihead_attn = MultiHeadAttention(d_model,nhead,dropout,beta,batch_first=True)
        self.multihead_attn = MultiHeadAttention(d_model,d_head=d_model,dropout=dropout,nhead=nhead,beta=beta)
        self.dropout1 = makeDropout(dropout)
        self.norm1 = torch.nn.LayerNorm(d_model)
        self.feedforward = FeedForward(d_model=d_model,dim_feedforward=d_model*4, dropout=dropout, beta=beta)
        self.dropout2 = makeDropout(dropout)
        self.norm2 = torch.nn.LayerNorm(d_model)
        self.alpha = alpha
    def forward(self, src, mask=None, src_key_padding_mask=None):
        src2,weight = self.multihead_attn(src, src, src,mask)
        src = src*self.alpha + self.dropout1(src2)
        src = self.norm1(src)
        src2 = self.feedforward(src)
        src = src*self.alpha + self.dropout2(src2)
        src = self.norm2(src)
        return src,weight

class MultiHeadAttention(torch.nn.Module):
    def __init__(self, d_q=512,d_head=-1,d_k=-1,d_v=-1, nhead=8, dropout=0.1, beta=1.0):
        super(MultiHeadAttention, self).__init__()
        self.beta = beta
        if d_head == -1:
            d_head = d_q//nhead
        if d_k == -1:
            d_k = d_q
        if d_v == -1:
            d_v = d_q
        self.wq = torch.nn.Linear(d_q, d_head*nhead)
        self.wk = torch.nn.Linear(d_k, d_head*nhead)
        self.wv = torch.nn.Linear(d_v, d_head*nhead)
        self.wo = torch.nn.Linear(d_head*nhead, d_q)
        self.dropout = makeDropout(dropout)
        self.nhead = nhead
        self.d_q=d_q
        self.d_head=d_head
        self.d_k=d_k
        self.d_v=d_v
        self.initialize()
    def initialize(self):
        torch.nn.init.xavier_uniform_(self.wq.weight, gain=1)
        torch.nn.init.xavier_uniform_(self.wk.weight, gain=1)
        torch.nn.init.xavier_uniform_(self.wv.weight, gain=self.beta)
        torch.nn.init.xavier_uniform_(self.wo.weight, gain=self.beta)
        #self.head_dim = d_model//nhead
    def forward_(self, q, k, v, mask=None):
        bs = q.size(0)
        q = self.wq(q).view(bs,-1,self.d_head,self.nhead)
        k = self.wk(k).view(bs,-1,self.d_head,self.nhead)
        v = self.wv(v).view(bs,-1,self.d_head,self.nhead)
        qk = torch.einsum('bqdh,bkdh->bqkh',q,k)/self.d_head**0.5
        if mask is not None:
            #print(mask.size())
            #qk = torch.einsum('bqkh,bk->bqkh',qk,mask)
            mask = mask.unsqueeze(2).transpose(1,3)
            qk = torch.where(mask+qk*0>0.01,qk,qk*0-1e9)
            #qk = qk.masked_fill(mask==-1e9)
        qk = torch.nn.functional.softmax(qk,dim=2)
        V = torch.einsum('bqkh,bkdh->bqdh',qk,v)
        V = V.reshape(bs,-1,self.d_head*self.nhead)
        output = self.wo(V)
        output = self.dropout(output)
        return output,qk
    def forward_(self, q, k, v, mask=None):
        bs = q.size(0)
        q = self.wq(q).view(bs,-1,self.nhead,self.d_head)
        k = self.wk(k).view(bs,-1,self.nhead,self.d_head)
        v = self.wv(v).view(bs,-1,self.nhead,self.d_head)
        #qk = torch.einsum('bqhd,bkhd->bqhk',q,k)/self.d_head**0.5
       
        # 假设 q 和 k 的形状分别是 (b, q, h, d) 和 (b, k, h, d)
        b, q_len, h, d = q.shape
        k_len = k.shape[1]

        # 1. 将 q 和 k reshape 为适合矩阵乘法的形状
        q_reshaped = q.permute(0, 2, 1, 3).reshape(b * h, q_len, d)  # (b * h, q, d)
        k_reshaped = k.permute(0, 2, 1, 3).reshape(b * h, k_len, d)  # (b * h, k, d)

        # 2. 进行矩阵乘法
        output = torch.matmul(q_reshaped.contiguous(), k_reshaped.transpose(-1, -2).contiguous())  # (b * h, q, k)

        # 3. 将输出 reshape 回 (b, q, h, k)
        qk = output.reshape(b, h, q_len, k_len).permute(0, 2, 1, 3)  # (b, q, h, k)

        if mask is not None:
            #print(mask.size())
            qk = torch.einsum('bqhk,bk->bqhk',qk,mask)
            #qk = qk.masked_fill(mask==-1e9)
        qk = torch.nn.functional.softmax(qk,dim=3)
        V = torch.einsum('bqhk,bkhd->bqhd',qk,v)
        V = V.reshape(bs,-1,self.d_head*self.nhead)
        output = self.wo(V)
        output = self.dropout(output)
        return output,qk
    def forward(self, q, k, v, mask=None):
        bs = q.size(0)
        q = self.wq(q).view(bs,-1,self.nhead,self.d_head)#.contiguous()
        k = self.wk(k).view(bs,-1,self.nhead,self.d_head)#.contiguous()
        v = self.wv(v).view(bs,-1,self.nhead,self.d_head)#.contiguous()
        qk = torch.einsum('bqhd,bkhd->bqhk',q,k)/self.d_head**0.5
        if mask is not None:
            qk = torch.einsum('bqhk,bk->bqhk',qk,mask)
        qk = torch.nn.functional.softmax(qk,dim=3)
        V = torch.einsum('bqhk,bkhd->bqhd',qk,v)
        V = V.reshape(bs,-1,self.d_head*self.nhead)
        output = self.wo(V)
        output = self.dropout(output)
        return output,qk
    
        
        
class UniEmbedding_(torch.nn.Module):
    def __init__(self, num_embeddings=512, embedding_dim=512, padding_idx=0, beta=1.0):
        super(UniEmbedding, self).__init__()
        self.embedding = torch.nn.Embedding(num_embeddings, embedding_dim, padding_idx=padding_idx)
        self.embedding_phase = torch.nn.Embedding(num_embeddings, embedding_dim, padding_idx=padding_idx)
        torch.nn.init.normal_(self.embedding.weight, mean=0, std=1)
        torch.nn.init.normal_(self.embedding_phase.weight, mean=0, std=1)
    def forward_(self, inputs,inputsType):
        bs = inputs.size(0)
        #inputsFlat = inputs.view(bs,-1,1)
        inputsTypeFlat = inputsType.view(bs,-1)
        inputsTypeFlatEmb = self.embedding(inputsTypeFlat)#bs, L*K
        #inputsTypeFlatEmbPhase = self.embedding_phase(inputsTypeFlat)
        
        
        index = torch.arange(150,150+inputs.size(-1),device=inputs.device,dtype=torch.long).view(1,1,-1)
        
        inputsTypeIndex = inputsType*0+index
        inputsTypeIndexFlat = inputsTypeIndex.view(bs,-1)#bs, L*K
        inputsTypeIndexFlatEmb = self.embedding(inputsTypeIndexFlat)
        
        inputsTypeIndexFlatEmbPhase = self.embedding_phase(inputsTypeIndexFlat)
        #print(inputsTypeIndexFlatEmb.size())    
        input_freq = (inputsTypeFlatEmb+inputsTypeIndexFlatEmb).view(bs,inputs.size(1),inputs.size(2),inputsTypeIndexFlatEmb.size(-1))
        
        output = torch.einsum('bijk,bij->bik',input_freq,inputs)
        
        return output  
    def forward(self, inputs,inputsType):
        bs = inputs.size(0)
        #inputsFlat = inputs.view(bs,-1,1)
        inputsTypeFlat = inputsType.view(bs,-1)
        inputsTypeFlatEmb = self.embedding(inputsTypeFlat)#bs, L*K
        inputsTypeFlatEmbPhase = self.embedding_phase(inputsTypeFlat)
        
        
        index = torch.arange(150,150+inputs.size(-1),device=inputs.device,dtype=torch.long).view(1,1,-1)
        
        inputsTypeIndex = inputsType*0+index
        inputsTypeIndexFlat = inputsTypeIndex.view(bs,-1)#bs, L*K
        inputsTypeIndexFlatEmb = self.embedding(inputsTypeIndexFlat)
        inputsTypeIndexFlatEmbPhase = self.embedding_phase(inputsTypeIndexFlat)
        
        #print(inputsTypeIndexFlatEmb.size())    
        input_freq = (inputsTypeFlatEmb+inputsTypeIndexFlatEmb).view(bs,inputs.size(1),inputs.size(2),inputsTypeIndexFlatEmb.size(-1))
        input_phase = (inputsTypeFlatEmbPhase+inputsTypeIndexFlatEmbPhase).view(bs,inputs.size(1),inputs.size(2),inputsTypeIndexFlatEmb.size(-1))
        input_freq = torch.exp(input_freq)
        inputs_d=inputs.unsqueeze(-1)*input_freq+input_phase
        #input_phase = torch.einsum('bijk,bij->bijk',input_freq,inputs+input_phase)
        output = torch.cos(inputs_d).sum(dim=-2)/inputs.size(-1)**0.5
        
        #input_freq = (inputsTypeFlatEmb+inputsTypeIndexFlatEmb).view(bs,inputs.size(1),inputs.size(2),inputsTypeIndexFlatEmb.size(-1))
        
        #output = torch.einsum('bijk,bij->bik',input_freq,inputs)
        
        return output    


def init_weights(weight,w_min,w_max):
    print(weight.size())
    #exit()
    N,H = weight.size()
    w0 = np.linspace(w_min,w_max,H)
    #np.random.shuffle(w0)
    weightL =[]
    #print(w0)
    #exit()
    for i in range(N):
        if i%H == 0:
            np.random.shuffle(w0)
        i = (np.arange(H)+i)%H
        weightL.append(w0[i%H])
    weight.data[:] = torch.tensor(np.array(weightL),dtype=weight.dtype,device=weight.device).view(N,H)
class UniEmbedding(torch.nn.Module):
    def __init__(self, num_embeddings=512, embedding_dim=512, padding_idx=0,dropout=0, beta=1.0,wave_idx=-1,segLength=-1):
        super(UniEmbedding, self).__init__()
        self.embedding_dim = embedding_dim
        
        #self.isSame = isSame
        self.embedding = torch.nn.Embedding(num_embeddings, embedding_dim//2, padding_idx=padding_idx)
        self.segLength = segLength
        self.wave_idx = wave_idx
        if segLength>0:
            self.conv = Conv(embedding_dim,segLength)
        self.embedding_w = torch.nn.Embedding(num_embeddings, embedding_dim//2, padding_idx=padding_idx)
        self.embedding_phase = torch.nn.Embedding(num_embeddings, embedding_dim//2, padding_idx=padding_idx)
        self.padding_idx = padding_idx
        init_weights(self.embedding.weight,-6,9)
        torch.nn.init.normal_(self.embedding_w.weight, mean=1, std=1e-4)
        torch.nn.init.xavier_uniform_(self.embedding_phase.weight, gain=3.1415926)
        self.dropout = makeDropout(dropout)
    def freez_freq(self):
        self.embedding.requires_grad = False
    def activate_freq(self):
        self.embedding.requires_grad = True
    def forward(self, inputs,inputsType):
        if self.segLength>0:
            wave = inputs[:,:,-self.segLength:]
            #isWave = torch.where(wave.sum(dim=-1,keepdim=True)==0,wave[:,:,:1]*0,wave[:,:,:1]*0+1)
            wave = self.conv(wave)#*isWave
            wave = self.dropout(wave)
            inputs = inputs[:,:,:-self.segLength]
            inputsType = inputsType[:,:,:-self.segLength]
        else:
            wave = 0
        
        inputsTypeIndex= torch.arange(1,1+inputs.size(-1),device=inputs.device,dtype=torch.long).view(1,1,-1)
        validM = (torch.where(inputsType==self.padding_idx,inputsType*0,inputsType*0+1)*torch.where(inputsType==self.wave_idx,inputsType*0,inputsType*0+1)).unsqueeze(-1)
        validCount = validM.sum(dim=-2,keepdim=True)
        validM = validM/validCount**0.5/2**0.5
        
        
        input_freq = torch.exp(self.embedding(inputsType))
        input_phase = self.embedding_phase(inputsTypeIndex)
        input_w =  self.embedding_w(inputsType)*validM
        
        inputs_d=inputs.unsqueeze(-1)*input_freq+input_phase
        output0 = (torch.cos(inputs_d)*input_w).sum(dim=-2)
        output1 = (torch.sin(inputs_d)*input_w).sum(dim=-2)
        output = torch.cat([output0,output1],dim=-1)+wave
        
        return output      
        
class Transformer(torch.nn.Module):
    def __init__(self, d_model=512, nhead=8, num_layers=6, dropout=0.1,outputN=1,isDeep=True,lossFunc=torch.nn.MSELoss()):
        super(Transformer, self).__init__()
        if isDeep:
            alpha = (2*num_layers)**0.25
            beta =  (8*num_layers)**(-0.25)
        else:
            alpha = 1
            beta = 1
        self.emb = UniEmbedding(256,d_model,)
        #print(len(list(self.parameters())))
        ABL = [AttentionBlock(d_model,nhead,dropout,beta,alpha) for i in range(num_layers)]
        #print(len(list(self.parameters())))
        self.ABL = torch.nn.ModuleList(ABL)
        #print(len(list(self.parameters())))
        #exit()
        self.denseOut = torch.nn.Linear(d_model,outputN)
        self.denseOutSigma = torch.nn.Linear(d_model,outputN)
        self.denseOutSigmaAc = torch.nn.Softplus()
        self.nhead = nhead
        self.lossFunc = lossFunc
       #self.atten = 
    def forward(self, inputs,inputsType,mask=None,need_weights=False):
        x = self.emb(inputs,inputsType)
        #print(x.size())
        #exit()
        #print('mask',mask.size())
        if mask is not None:
            #print(mask.size())
            mask = mask.squeeze(-1)#.unsqueeze(3)
            #
            #mask = mask.view(-1,1,1,mask.size(1))
            #print(mask.size())
            #mask = mask.repeat(1,self.nhead,x.size(1),1)
            #print(mask.size())
            #mask = mask.view(-1,mask.size(2),mask.size(3))
        weightL = []
        for abl in self.ABL:
            x,weight = abl(x,mask)
            #print(x.size())
            weightL.append(weight)
        output = self.denseOut(x)
        outputSigma = self.denseOutSigma(x)
        outputSigma = self.denseOutSigmaAc(outputSigma)
        output = torch.cat([output,outputSigma],dim=-1)
        return output,weightL
    def freeze_freq(self):
        self.emb.freez_freq()
    def activate_freq(self):
        self.emb.activate_freq()
    def Predict(self,inputs,inputsType,mask0,outputs,outputsType,mask1):
        if not isinstance(mask0,torch.Tensor):
            inputsType = inputsType.astype('int64')
            outputsType = outputsType.astype('int64')
            inputs = inputs.astype('float32')   
            outputs = outputs.astype('float32')
            mask0 = mask0.astype('float32')
            mask1 = mask1.astype('float32')
            inputs = torch.from_numpy(inputs).to(device=self.emb.embedding.weight.device)
            inputsType = torch.from_numpy(inputsType).to(device=self.emb.embedding.weight.device)
            mask0 = torch.from_numpy(mask0).to(device=self.emb.embedding.weight.device)
            outputs = torch.from_numpy(outputs).to(device=self.emb.embedding.weight.device)
            outputsType = torch.from_numpy(outputsType).to(device=self.emb.embedding.weight.device)
            mask1 = torch.from_numpy(mask1).to(device=self.emb.embedding.weight.device)
        inputs0 = torch.cat([inputs,outputs],dim=1)
        inputsType0 = torch.cat([inputsType,outputsType],dim=1)
        outputs_L = outputs.size(1)
        mask = torch.cat([mask0,mask1],dim=1)
        output,_ = self.forward(inputs0,inputsType0,mask)
        return output[:,-outputs_L:,:]
    def predict(self,inputs,inputsType,mask0,outputs,outputsType,mask1,batch_size=32):
        with torch.no_grad():
            outputs_L = []
            for i in range(0,inputs.shape[0],batch_size):
                output = self.Predict(inputs[i:i+batch_size],inputsType[i:i+batch_size],mask0[i:i+batch_size],outputs[i:i+batch_size],outputsType[i:i+batch_size],mask1[i:i+batch_size]).cpu().detach().numpy()
                outputs_L.append(output)
            return np.concatenate(outputs_L,axis=0)
            #return self.Predict(inputs,inputsType,mask0,outputs,outputsType,mask1).cpu().detach().numpy()
    def fit(self,inputs,inputsType,mask0,outputs,outputsType,mask1,labels,opt,batch_size=32):
        self.train()
        lossL = []
        stime = time()
        for i in range(0,inputs.shape[0],batch_size):
            #print(i//batch_size,inputs.shape[0]//batch_size)
            opt.zero_grad()
            output = self.Predict(inputs[i:i+batch_size],inputsType[i:i+batch_size],mask0[i:i+batch_size],outputs[i:i+batch_size],outputsType[i:i+batch_size],mask1[i:i+batch_size])
            labels0 = torch.from_numpy(labels[i:i+batch_size]).to(device=self.emb.embedding.weight.device)
            loss = self.lossFunc(labels0,output)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
            opt.step()
            lossL.append(loss.item())
        pertime = (time()-stime)/inputs.shape[0]
        print(np.mean(lossL),f'{pertime:.6f}s')
        return np.mean(lossL)
    def evaluate(self,inputs,inputsType,mask0,outputs,outputsType,mask1,labels):
        output = self.predict(inputs,inputsType,mask0,outputs,outputsType,mask1)
        loss = self.lossFunc(labels,output)
        return loss.item()
    def attention(self,inputs,inputsType,mask0,outputs,outputsType,mask1):
        with torch.no_grad():
            inputs0 = torch.cat([inputs,outputs],dim=1)
            inputsType0 = torch.cat([inputsType,outputsType],dim=1)
            outputs_L = outputs.size(1)
            mask = torch.cat([mask0,mask1],dim=1)
            _,weightL = self.forward(inputs0,inputsType0,mask)
            return torch.cat(weightL,dim=0)[:,:,-outputs_L:,-outputs_L:].cpu().detach().numpy()
backend = torch      
def huber(y_true, y_pred,delta=0.05):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
    else:
        weight = 1.0
    error = y_true - y_pred
    error = backend.where(backend.abs(error)<delta,0.5*backend.square(error),delta*(backend.abs(error)-0.5*delta))
    W = backend.where(y_true>900,0.0, weight)
    W=W/backend.mean(W)
    return backend.mean(error*W)
def withSigma(y_true, y_pred,delta=3.0):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if isinstance(y_true,torch.Tensor):
        backend = torch
    else:
        backend = np
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
        #weight = weight /K.mean(weight)
    else:
        weight = 1.0
    error = (y_true - y_pred)/y_sigma
    Sigma = backend.log(y_sigma)
    error = backend.where(backend.abs(error)<delta,0.5*backend.square(error),delta*(backend.abs(error)-0.5*delta))
    W = backend.where(y_true>900,0.0,weight)
    W=W/backend.mean(W)
    return backend.mean(error*W)+backend.mean(Sigma*W)

def withSigma0(y_true, y_pred,delta=3):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
        #weight = weight /K.mean(weight)
    else:
        weight = 1.0
    y_sigma0 = 0.1
    error = (y_true - y_pred)/y_sigma0
    Sigma = backend.square(y_sigma/y_sigma0-1)
    error = backend.where(backend.abs(error)<delta,0.5*backend.square(error),delta*(backend.abs(error)-0.5*delta))
    W = backend.where(y_true>900,0.0,weight)
    W=W/backend.mean(W)
    return backend.mean(error*W)+backend.mean(Sigma*W)
def MSE(y_true, y_pred):
    y_pred,y_sigma = y_pred[:,:,:1],y_pred[:,:,1:]
    if y_true.shape[-1]>1:
        weight = y_true[:,:,1:]
        y_true = y_true[:,:,:1]
    else:
        weight = 1.0
    W = backend.where(y_true>900,0.0,weight)
    W=W/backend.mean(W)
    return backend.mean(backend.square(y_true - y_pred)*W)

lossD = {'MSE':MSE,'huber':huber,'withSigma':withSigma,'l1':'l1'}#


if __name__ == '__main__':
    
    import torch
    #if False
    a = MultiHeadAttention(160,8)
    count = 0
    for p in a.parameters():
        count+=p.numel()
        #print(p.shape)
    print(count)
    b = AttentionBlock(160,10)
    count = 0
    for p in b.parameters():
        count+=p.numel()
        #print(p.shape)
    print(count)
    #exit()
    #emb = UniEmbedding(512,512)
    trans = Transformer(160,10,24,0.1)
    count = 0
    for p in trans.parameters():
        count+=p.numel()
    print(count)
    #exit()
    inputs = torch.randint(0,128,(64,105,10)).float()
    inputsType = torch.randint(0,128,(64,105,10))
    mask = torch.randint(0,2,(64,105,1)).float()
    
    outputs = torch.randint(0,128,(64,5,10)).float()
    outputsType = torch.randint(0,128,(64,5,10))
    mask1 = torch.randint(0,2,(64,5,1)).float()
    
    #output = emb(inputs,inputsType)
    #print(output.size()) 
    #print(output)
    #outputTrans,weight = trans(inputs,inputsType)
    #print(outputTrans.size(),weight[0].size())
    trans.to('cuda')
    inputs = inputs.to('cuda')
    inputsType = inputsType.to('cuda')
    mask = mask.to('cuda')
    outputs = outputs.to('cuda')
    outputsType = outputsType.to('cuda')
    mask1 = mask1.to('cuda')
    
    pre = trans.predict(inputs,inputsType,mask,outputs,outputsType,mask1)
    stime = time()
    for i in range(100):
        print(i)
        pre = trans.predict(inputs,inputsType,mask,outputs,outputsType,mask1)
    print((time()-stime)/100)  
    print(pre.shape)
def collate_function(dataL):
    result =[]
    for i in range(len(dataL[0])):
        result.append(np.concatenate([data[i][np.newaxis,:] for data in dataL]))
    return result